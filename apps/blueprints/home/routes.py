from apps.blueprints.home import blueprint
from flask import render_template, request, redirect, url_for, jsonify, flash
import pandas as pd
from datetime import datetime
from apps.extensions import db
from apps.utils.income_statement import get_income_statement_data
from apps.repositories.journal_entries import get_journal_entries, add_journal_entry
from apps.repositories.transactions import get_transactions, add_transaction
from apps.repositories.accounts import (
    get_all_accounts, get_accounts_by_type,
    get_payment_account_id, get_account_details
)
from apps.repositories.common import (
    get_assets,
    get_liabilities,
    get_total_assets,
    get_total_liabilities,
    get_total_expense,
    get_total_income
)

@blueprint.route('/', methods=['GET'])
@blueprint.route('/home', methods=['GET'])
@blueprint.route('/dashboard', methods=['GET'])
def index():
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')

    # get data
    income_data, expense_data, total_income, total_expense, net_income = get_income_statement_data(start_date, end_date)

    # get total liability amount
    total_liability = get_total_liabilities(start_date, end_date)
    # get total assets amount
    total_asset = get_total_assets(start_date, end_date)
    # total equity
    total_equity = total_asset + net_income - total_liability
    # Group by date and sum amounts for both income and expenses
    income_grouped = income_data.groupby('date').sum().rename(columns={'amount': 'total_income'})
    expense_grouped = expense_data.groupby('date').sum().rename(columns={'amount': 'total_expense'})

    # Merge the income and expense data on the 'date' column
    merged_df = pd.merge(income_grouped, expense_grouped, on='date', how='outer').fillna(0)

    # Calculate net income per date
    merged_df['net_income'] = merged_df['total_income'] - merged_df['total_expense']
    merged_df.reset_index(inplace=True)
    records = merged_df.to_dict('records')
    for record in records:
        record['date'] = str(record['date']) 

    print("total_income:", total_income)
    print("total_expense:", total_expense)
    print("net worth:", total_equity)
    print("total liability amount:", total_liability)
    print("total asset amount:", total_asset)
    print("total liability amount:", total_liability)
    print("income data:", income_data)
    print("expense data:", expense_data)

    # Render the template with data
    return render_template(
        'home/pages/dashboard.html',
        records=records,
        total_income = total_income,
        total_expense = total_expense,
        total_equity = total_equity,
        total_liability = total_liability,
        total_asset = total_asset,
        # extra
        net_income = net_income,
        page_name="dashboard",
        start_date=start_date,
        end_date=end_date)

@blueprint.route('/add', methods=['GET', 'POST'])
def add():
    print('add transaction')
    if request.method == 'POST':
        # Get form data
        transaction_name = request.form['transactionName']
        description = request.form['description']
        amount = float(request.form['amount'])
        payment_type = request.form['paymentType']
        date = request.form['date']
        print("Date:",date)
        selected_type = request.form['accountType']
        selected_account_name = request.form['accountName']

        # Convert date string to datetime.date
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'error')
            return redirect(url_for('add'))
        
        # Fetch account details
        accounts = get_accounts_by_type(selected_type)
        account_ids = [account[0] for account in accounts]
        account_names = [account[1] for account in accounts]
        selected_account_id = account_ids[account_names.index(selected_account_name)]

        if selected_account_id:
            # Add transaction
            transaction_id = add_transaction(
                transaction_name=transaction_name,
                account_id=selected_account_id,
                description=description,
                amount=amount,
                payment_type=payment_type,
                date=date
            )

            # Add journal entries
            payment_account_id = get_payment_account_id(selected_type, payment_type)
            account_name, account_type = get_account_details(selected_account_id)

            if account_type == 'Income':
                add_journal_entry(transaction_id, selected_account_id, 'credit', amount, date)
                add_journal_entry(transaction_id, payment_account_id, 'debit', amount, date)
                
            elif account_type == 'Expense':
                add_journal_entry(transaction_id, selected_account_id, 'debit', amount, date)
                add_journal_entry(transaction_id, payment_account_id, 'credit', amount, date)

            elif account_type == 'Asset':
                add_journal_entry(transaction_id, selected_account_id, 'debit', amount, date)
                add_journal_entry(transaction_id, payment_account_id, 'credit', amount, date)
                
            elif account_type == 'Liability':
                add_journal_entry(transaction_id, selected_account_id, 'credit', amount, date)
                add_journal_entry(transaction_id, payment_account_id, 'debit', amount, date)

            elif account_type == 'Equity':
                add_journal_entry(transaction_id, selected_account_id, 'credit', amount, date)
                add_journal_entry(transaction_id, payment_account_id, 'debit', amount, date)

            flash('Transaction and journal entries added successfully.', 'success')
            return redirect(url_for('home_blueprint.add'))
        else:
            flash('Please select a valid account.', 'error')

    # GET request: Render the form
    # get all accounts for account selection
    accounts = get_all_accounts()
    account_dict = {}
    
    # Iterate over all accounts
    for account in accounts:
        # Get account_type and account_name
        if account.account_type != "Equity" and account.account_name not in ['Cash', 'Credit Card', 'Debit Card', 'Bank Transfer']:
            account_type = account.account_type
            account_name = account.account_name
        
        # If the account_type is not already a key in the dictionary, add it with an empty list
        if account_type not in account_dict:
            account_dict[account_type] = []
        
        # Append the account_name to the appropriate list
        account_dict[account_type].append(account_name)
    
    return render_template('home/pages/add_transactions.html', accounts=account_dict , page_name = 'add_transactions')

@blueprint.route('/transactions', methods=['GET'])
def transactions():
    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')

    # Fetch transactions data
    data, total_count = get_transactions(start_date, end_date, page, per_page)
    print("data:", data)

    # Calculate total pages
    total_pages = (total_count + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'home/pages/transactions.html',
        transactions=data,
        page_name="transactions",
        page_no = page,
        total_pages=total_pages,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date
    )

@blueprint.route('/journal', methods=['GET'])
def journal():
    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default to page 1
    per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')

    # Fetch the journal entries data
    data, total_count = get_journal_entries(start_date, end_date, page, per_page)
    # data = pd.DataFrame(data, columns=['entry_id', 'transaction_name', 'account_name', 'transaction_type', 'amount', 'date'])

    total_pages = (total_count + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'home/pages/journal_entries.html',
        journal_entries=data,
        page_name="journal_entries",
        page_no = page,
        total_pages=total_pages,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date)

@blueprint.route('/ledger')
def ledger():
    return render_template('home/pages/general_ledger.html',
                           page_name="general_ledger",
                           )

@blueprint.route('/statement', methods=['GET'])
def statement():
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')

    # Fetch the journal entries data
    income_data, expense_data, total_income, total_expense, net_income = get_income_statement_data(start_date, end_date)
    # data = pd.DataFrame(data, columns=['entry_id', 'transaction_name', 'account_name', 'transaction_type', 'amount', 'date'])

    print("income:", income_data)
    print("expense:", expense_data)
    print("total_income:", total_income)
    print("total_expense:", total_expense)
    print("net income:", net_income)

    # total_pages = (total_count + per_page - 1) // per_page

    # Render the template with data
    return render_template(
        'home/pages/income_statement.html',
        income_data=income_data,
        expense_data = expense_data,
        total_income = total_income,
        total_expense = total_expense,
        net_income = net_income,
        page_name="income_statement",
        start_date=start_date,
        end_date=end_date)


@blueprint.route('/sheet', methods=['GET'])
def sheet():
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', '2024-12-31')

    # get total assets
    all_assets = get_assets(start_date, end_date)
    # get total liabilities
    all_liabilities = get_liabilities(start_date, end_date)
    # net income
    total_income = get_total_income(start_date, end_date)
    total_expense = get_total_expense(start_date, end_date)
    net_income = total_income - total_expense
    # get total liability amount
    total_liability = get_total_liabilities(start_date, end_date)
    # get total assets amount
    total_asset = get_total_assets(start_date, end_date)
    # total equity
    total_equity = total_asset + net_income - total_liability

    # Fetch the journal entries data
    # income_data, expense_data, total_income, total_expense, net_income = get_income_statement_data(start_date, end_date)
    # data = pd.DataFrame(data, columns=['entry_id', 'transaction_name', 'account_name', 'transaction_type', 'amount', 'date'])

    print("liabilities:", all_liabilities)
    print("assets:", all_assets)
    print("total_income:", total_income)
    print("total_expense:", total_expense)
    print("net income:", net_income)
    print("total liability amount:", total_liability)
    print("total asset amount:", total_asset)

    # Render the template with data
    return render_template(
        'home/pages/balance_sheet.html',
        liabilities=all_liabilities,
        assets = all_assets,
        net_income = net_income,
        retained_earning = net_income, #assuming no dividends
        total_liability=total_liability,
        total_asset=total_asset,
        total_equity = total_equity,
        page_name="balance_sheet",
        start_date=start_date,
        end_date=end_date)
