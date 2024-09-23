from flask import Flask
from importlib import import_module
from apps.extensions import db, moment
from apps.models.accounts import Accounts
# from apps.models.commons import add_regions_bulk
import os

def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    # for module_name in ('authentication', 'home'):
    module = import_module('apps.blueprints.home.routes')
    print('home', module.blueprint)
    app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_request
    def initialize_database():
        app.before_request_funcs[None].remove(initialize_database)
        try:
            db.create_all()
            
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ESOAI.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

            print('> Fallback to SQLite ')
            db.create_all()

        # Define the initial data
        accounts_data = [
            # Expense
            ('Groceries', 'Expense'),
            ('Rent', 'Expense'),
            ('Utilities', 'Expense'),
            ('Transportation', 'Expense'),
            ('Entertainment', 'Expense'),
            ('Health Expenses', 'Expense'),
            ('Insurance', 'Expense'),
            ('Dining Out', 'Expense'),
            ('Subscriptions', 'Expense'),
            ('Miscellaneous', 'Expense'),
            ('Other', 'Expense'),
            ('Cash', 'Expense'),
            ('Bank Transfer', 'Expense'),
            ('Credit Card', 'Expense'),
            ('Debit Card', 'Expense'),
            # Income
            ('Salary Income', 'Income'),
            ('Freelance Income', 'Income'),
            ('Investment Income', 'Income'),
            ('Rental Income', 'Income'),
            ('Other', 'Income'),
            ('Cash', 'Income'),
            ('Bank Transfer', 'Income'),
            ('Credit Card', 'Income'),
            ('Debit Card', 'Income'),
            # Asset
            ('Cash', 'Asset'),
            ('Bank Account', 'Asset'),
            ('Savings Account', 'Asset'),
            ('Investments', 'Asset'),
            ('Property', 'Asset'),
            ('Car', 'Asset'),
            ('Personal Belongings', 'Asset'),
            ('Other', 'Asset'),
            ('Bank Transfer', 'Asset'),
            ('Credit Card', 'Asset'),
            ('Debit Card', 'Asset'),
            # Liability
            ('Credit Card', 'Liability'),
            ('Personal Loan', 'Liability'),
            ('Mortgage', 'Liability'),
            ('Car Loan', 'Liability'),
            ('Student Loan', 'Liability'),
            ('Taxes Payable', 'Liability'),
            ('Other', 'Liability'),
            ('Cash', 'Liability'),
            ('Bank Transfer', 'Liability'),
            ('Debit Card', 'Liability'),
            # Equity
            ('Owner\'s Equity', 'Equity'),
            ('Cash', 'Equity'),
            ('Bank Transfer', 'Equity'),
            ('Debit Card', 'Equity'),
            ('Credit Card', 'Equity'),
        ]

        # Add accounts to the database
        for account_name, account_type in accounts_data:
            account = Accounts(account_name=account_name, account_type=account_type)
            db.session.add(account)
        
        # Commit the changes
        db.session.commit()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

# from apps.authentication.oauth import github_blueprint

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
