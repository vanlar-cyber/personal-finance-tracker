from apps import db
from apps.models.transactions import Transactions
from apps.models.accounts import Accounts
import pandas as pd

def get_assets(start_date, end_date):
    # Query to get total assets
    assets_query = db.session.query(
        Accounts.account_name,
        Transactions.amount,
        Transactions.date
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Asset') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .group_by(Accounts.account_name).all()

    # Convert to DataFrame for further processing if needed
    assets_df = pd.DataFrame(assets_query, columns=['Account', 'Amount','Date'])

    return assets_df

def get_liabilities(start_date, end_date):
    # Query to get total liabilities
    liabilities_query = db.session.query(
        Accounts.account_name,
        Transactions.amount,
        Transactions.date
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Liability') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .group_by(Accounts.account_name).all()

    # Convert to DataFrame for further processing if needed
    liabilities_df = pd.DataFrame(liabilities_query, columns=['Account', 'Amount','Date'])

    return liabilities_df

def get_total_income(start_date, end_date):
    # Query to get total income
    total_income_query = db.session.query(
        db.func.sum(Transactions.amount).label('total_income')
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Income') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .scalar()  # Use scalar() to get a single value

    # Return total income or 0.0 if no result
    total_income = total_income_query if total_income_query else 0.0

    return total_income

def get_total_expense(start_date, end_date):
    # Query to get total expenses
    total_expense_query = db.session.query(
        db.func.sum(Transactions.amount).label('total_expense')
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Expense') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .scalar()  # Use scalar() to get a single value

    # Return total expense or 0.0 if no result
    total_expense = total_expense_query if total_expense_query else 0.0

    return total_expense

def get_total_assets(start_date, end_date):
    # Query to get total assets
    total_assets_query = db.session.query(
        db.func.sum(Transactions.amount)
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Asset') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .scalar()  # Use scalar() to get a single value

    # Return total assets or 0.0 if no result
    total_assets = total_assets_query if total_assets_query else 0.0

    return total_assets


def get_total_liabilities(start_date, end_date):
    # Query to get total liabilities
    total_liabilities_query = db.session.query(
        db.func.sum(Transactions.amount)
    ).join(Accounts, Transactions.account_id == Accounts.id) \
    .filter(Accounts.account_type == 'Liability') \
    .filter(Transactions.date.between(start_date, end_date)) \
    .scalar()  # Use scalar() to get a single value

    # Return total liabilities or 0.0 if no result
    total_liabilities = total_liabilities_query if total_liabilities_query else 0.0

    return total_liabilities
