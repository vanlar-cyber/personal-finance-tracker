from apps.extensions import db

class GeneralLedger(db.Model):
    __tablename__ = 'general_ledger'
    
    ledger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)  # Foreign key to accounts table
    debit = db.Column(db.Float)  # Debit amount
    credit = db.Column(db.Float)  # Credit amount
    balance = db.Column(db.Float)  # Account balance
    date = db.Column(db.Date, nullable=False)  # Date of ledger entry
    
    # Relationship with Account model
    account = db.relationship('Accounts', backref=db.backref('general_ledgers', lazy=True))
    
    def __repr__(self):
        return f'<GeneralLedger Account: {self.account_id}, Balance: {self.balance}>'
    