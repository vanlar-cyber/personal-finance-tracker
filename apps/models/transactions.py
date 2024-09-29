from apps.extensions import db

class Transactions(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_name = db.Column(db.String, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False) 
    description = db.Column(db.String) 
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String, nullable=False) 
    date = db.Column(db.Date, nullable=False) 
    
    __table_args__ = (
        db.CheckConstraint("payment_type IN ('Cash', 'Credit Card', 'Debit Card', 'Bank Transfer')", name='payment_type_check'),
    )
    
    account = db.relationship('Accounts', backref=db.backref('transactions', lazy=True))
    
    def __repr__(self):
        return f'<Transaction {self.transaction_name} - {self.amount}>'
    