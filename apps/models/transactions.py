from apps.extensions import db

class Transactions(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_name = db.Column(db.String, nullable=False)  # Name of the transaction
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)  # Foreign key to accounts table
    description = db.Column(db.String)  # Detailed description of the transaction
    amount = db.Column(db.Float, nullable=False)  # Amount involved in the transaction
    payment_type = db.Column(db.String, nullable=False)  # Payment method
    date = db.Column(db.Date, nullable=False)  # Date of transaction
    
    # Ensuring payment_type has a limited set of values
    __table_args__ = (
        db.CheckConstraint("payment_type IN ('Cash', 'Credit Card', 'Debit Card', 'Bank Transfer')", name='payment_type_check'),
    )
    
    # Relationship with the Account model
    account = db.relationship('Accounts', backref=db.backref('transactions', lazy=True))
    
    def __repr__(self):
        return f'<Transaction {self.transaction_name} - {self.amount}>'
    