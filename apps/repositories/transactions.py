from apps import db
from apps.models.transactions import Transactions
from apps.models.accounts import Accounts
import pandas as pd

def add_transaction(transaction_name, account_id, description, amount, payment_type, date):
    new_transaction = Transactions(
        transaction_name=transaction_name,
        account_id=account_id,
        description=description,
        amount=amount,
        payment_type=payment_type,
        date=date
    )
    
    db.session.add(new_transaction)
    db.session.commit()
    
    return new_transaction.transaction_id

def get_transactions(start_date, end_date, page, per_page):
    offset = (page - 1) * per_page
    # Example query with SQLAlchemy
    transactions = db.session.query(
        Transactions.transaction_id,
        Transactions.transaction_name,
        Accounts.account_type,
        Transactions.description,
        Transactions.amount,
        Transactions.payment_type,
        Transactions.date
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Transactions.date.between(start_date, end_date)) \
    .order_by(Transactions.date.desc()) \
    .offset(offset) \
    .limit(per_page) \
    .all()

    total_count = db.session.query(Transactions).filter(Transactions.date.between(start_date, end_date)).count()
    
    return transactions, total_count

def get_transactions_with_details(start_date, end_date):
    # Query to get account details along with transaction amounts
    results = db.session.query(
        Accounts.account_name,
        Accounts.account_type,
        Transactions.amount,
        Transactions.date
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Transactions.date.between(start_date, end_date)) \
    .all()

    # Convert to DataFrame for further processing if needed
    # transactions_df = pd.DataFrame(query, columns=['Account Name', 'Account Type', 'Amount'])
    transactions_df = pd.DataFrame(results, columns=['account_name', 'account_type', 'amount','date'])

    return transactions_df
