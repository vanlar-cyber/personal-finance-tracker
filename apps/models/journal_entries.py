from apps.extensions import db


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'
    
    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False) 
    transaction_type = db.Column(db.String, nullable=False)  
    amount = db.Column(db.Float, nullable=False)  
    date = db.Column(db.Date, nullable=False) 
    
    __table_args__ = (
        db.CheckConstraint("transaction_type IN ('debit', 'credit')", name='transaction_type_check'),
    )
    
    transaction = db.relationship('Transactions', backref=db.backref('journal_entries', lazy=True))
    account = db.relationship('Accounts', backref=db.backref('journal_entries', lazy=True))
    
    def __repr__(self):
        return f'<JournalEntry {self.transaction_type} - {self.amount}>'
    