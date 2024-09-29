from apps.extensions import db

class GeneralLedger(db.Model):
    __tablename__ = 'general_ledger'
    
    ledger_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False) 
    debit = db.Column(db.Float) 
    credit = db.Column(db.Float) 
    balance = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False)
    
    account = db.relationship('Accounts', backref=db.backref('general_ledgers', lazy=True))
    
    def __repr__(self):
        return f'<GeneralLedger Account: {self.account_id}, Balance: {self.balance}>'
    