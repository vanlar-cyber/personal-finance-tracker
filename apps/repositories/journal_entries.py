from apps import db
from apps.models.journal_entries import JournalEntry
from apps.models.transactions import Transactions
from apps.models.accounts import Accounts

def add_journal_entry(transaction_id, account_id, transaction_type, amount, date):
    new_entry = JournalEntry(
        transaction_id=transaction_id,
        account_id=account_id,
        transaction_type=transaction_type,
        amount=amount,
        date=date
    )
    
    db.session.add(new_entry)
    db.session.commit()

def get_journal_entries(start_date, end_date, page, per_page):
    # Query to get journal entries within the specified date range
    offset = (page - 1) * per_page
    result = db.session.query(
        JournalEntry.entry_id,
        Transactions.transaction_name,
        Accounts.account_name,
        JournalEntry.transaction_type,
        JournalEntry.amount,
        JournalEntry.date
    ).join(Transactions, JournalEntry.transaction_id == Transactions.transaction_id) \
    .join(Accounts, JournalEntry.account_id == Accounts.id) \
    .filter(JournalEntry.date.between(start_date, end_date)) \
    .offset(offset) \
    .limit(per_page) \
    .all()
    total_count = db.session.query(JournalEntry).filter(JournalEntry.date.between(start_date, end_date)).count()

    return result, total_count
