from flask_sqlalchemy import SQLAlchemy
from apps import db
from apps.models.transactions import Transactions
from apps.models.accounts import Accounts
import pandas as pd
from apps.repositories.common import (
    get_assets_query, get_liabilities_query, get_total_income, get_total_expense
)

def get_balance_sheet_data(start_date, end_date):
    # Calculate Total Assets
    assets_df = get_assets_query(start_date, end_date)
    total_assets = assets_df['Amount'].sum() if not assets_df.empty else 0.0

    # Calculate Total Liabilities
    liabilities_df = get_liabilities_query(start_date, end_date)
    total_liabilities = liabilities_df['Amount'].sum() if not liabilities_df.empty else 0.0

    # Calculate Total Income
    total_income = get_total_income(start_date, end_date)

    # Calculate Total Expense
    total_expense = get_total_expense(start_date, end_date)

    # Net Income
    net_income = total_income - total_expense

    # Total Assets including Net Income
    total_assets_including_net_income = total_assets + net_income

    # Retained Earnings
    retained_earnings = net_income - total_assets

    # Total Equity
    total_equity = retained_earnings

    # Balance Check
    balance_check = total_assets_including_net_income - (total_liabilities + total_equity)

    return assets_df, liabilities_df, net_income, total_assets, total_liabilities, retained_earnings, total_equity, balance_check
