from apps.repositories.common import (
    get_total_income,
    get_total_expense,
    get_total_assets,
    get_total_liabilities
)

def calculate_totals(start_date, end_date):
    # Calculate total income
    total_income = get_total_income(start_date, end_date)
    
    # Calculate total expenses
    total_expenses = get_total_expense(start_date, end_date)
    
    # Calculate total assets
    total_assets = get_total_assets(start_date, end_date)
    
    # Calculate total liabilities
    total_liabilities = get_total_liabilities(start_date, end_date)
    
    
    # Calculate net worth
    net_worth = total_assets - total_liabilities + total_income - total_expenses
    
    return total_income, total_expenses, total_assets, total_liabilities, net_worth

# def plot_spending_trends(start_date, end_date):
#     conn = sqlite3.connect('personal_finance.db')
#     query = """
#         SELECT t.date, a.account_type, t.amount
#         FROM transactions t
#         JOIN accounts a ON t.account_id = a.id
#         WHERE t.date BETWEEN ? AND ?
#     """
#     df = pd.read_sql_query(query, conn, params=(start_date, end_date))
#     conn.close()
    
#     # Convert date to datetime for better plotting
#     df['date'] = pd.to_datetime(df['date'])
    
#     # Aggregate data: Sum amounts for the same date and account type
#     df_aggregated = df.groupby(['date', 'account_type'], as_index=False)['amount'].sum()
    
#     # Sort data by date
#     df_aggregated = df_aggregated.sort_values(by='date')
    
#     # Create a Plotly figure with lines and markers
#     fig = go.Figure()
    
#     # Add line and scatter traces for each account type
#     for account_type in df_aggregated['account_type'].unique():
#         df_filtered = df_aggregated[df_aggregated['account_type'] == account_type]
        
#         # Add line trace
#         fig.add_trace(go.Scatter(
#             x=df_filtered['date'],
#             y=df_filtered['amount'],
#             mode='lines+markers',  # Lines with markers
#             name=account_type
#         ))
    
#     # Update layout to improve appearance
#     fig.update_layout(
#         title='Trends of Income, Expenses, Assets, and Liabilities Over Time',
#         xaxis_title='Date',
#         yaxis_title='Amount',
#         xaxis=dict(tickformat='%Y-%m-%d'),  # Format x-axis as date
#         legend_title='Account Type',
#         template='plotly_white'
#     )
    
#     # Display the figure
#     st.plotly_chart(fig)