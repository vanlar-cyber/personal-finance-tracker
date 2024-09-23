from apps.extensions import db

class Accounts(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_name = db.Column(db.String, nullable=False)
    account_type = db.Column(db.String, nullable=False)
    
    # Ensuring account_type has a limited set of values
    __table_args__ = (
        db.CheckConstraint("account_type IN ('Income', 'Expense', 'Asset', 'Liability', 'Equity')", name='account_type_check'),
    )
    
    def __repr__(self):
        return f'<Account {self.account_name}>'
