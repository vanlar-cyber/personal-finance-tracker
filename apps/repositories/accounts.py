from apps import db
from apps.models.accounts import Accounts

def get_all_accounts():
    # Fetch all accounts from the database
    accounts = Accounts.query.all()
    return accounts

def get_account_details(account_id):
    account = Accounts.query.filter_by(id=account_id).first()
    if account:
        return account.account_name, account.account_type
    else:
        return None, None

def get_payment_account_id(account_type, payment_type):
    account = Accounts.query.filter_by(account_name=payment_type, account_type=account_type).first()
    if account:
        return account.id
    else:
        return None
    
def get_accounts_by_type(account_type):
    accounts = db.session.query(Accounts.id, Accounts.account_name).filter(
        Accounts.account_type == account_type,
        Accounts.account_name.notin_(['Cash', 'Credit Card', 'Debit Card', 'Bank Transfer'])
    ).all()

    return accounts

def get_account_types():
    # Query to get distinct account types excluding 'Equity'
    account_types = db.session.query(Accounts.account_type).distinct().filter(Accounts.account_type != 'Equity').all()
    # Extract the types from the query result
    account_types = [at[0] for at in account_types]
    return account_types
