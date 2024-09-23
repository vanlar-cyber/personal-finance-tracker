from apps.repositories.transactions import get_transactions_with_details

def get_income_statement_data(start_date, end_date):
    data = get_transactions_with_details(start_date,end_date)
    print("Results:", data)
    # Filter data for income and expenses
    income_data = data[data['account_type'] == 'Income']
    expense_data = data[data['account_type'] == 'Expense']
    
    # Calculate totals
    total_income = income_data['amount'].sum()
    total_expense = expense_data['amount'].sum()
    net_income = total_income - total_expense

    # Prepare income and expense data for display
    # income_df = income_data[['account_name', 'amount']].rename(columns={'account_name': 'Income Account', 'amount': 'Amount ($)'})
    # expense_df = expense_data[['account_name', 'amount']].rename(columns={'account_name': 'Expense Account', 'amount': 'Amount ($)'})

    return income_data, expense_data, total_income, total_expense, net_income

# def display_income_statement(data, start_date, end_date):
#     # Display header with date range
#     st.info(f"Income Statement ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
    
#     # Filter data for income and expenses
#     income_data = data[data['account_type'] == 'Income']
#     expense_data = data[data['account_type'] == 'Expense']
    
#     # Calculate totals
#     total_income = income_data['amount'].sum()
#     total_expense = expense_data['amount'].sum()
#     net_income = total_income - total_expense

#     # Prepare income and expense data for display
#     if not income_data.empty:
#         income_df = income_data[['account_name', 'amount']].rename(columns={'account_name': 'Income Account', 'amount': 'Amount ($)'})
#     else:
#         income_df = pd.DataFrame(columns=['Income Account', 'Amount ($)'])
    
#     if not expense_data.empty:
#         expense_df = expense_data[['account_name', 'amount']].rename(columns={'account_name': 'Expense Account', 'amount': 'Amount ($)'})
#     else:
#         expense_df = pd.DataFrame(columns=['Expense Account', 'Amount ($)'])

#     # Create two columns for Income and Expense
#     col1, col2 = st.columns(2)

#     with col1:
#         st.write("#### Income")
#         gd_income = GridOptionsBuilder.from_dataframe(income_df)
#         gd_income.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=5)  # Paginate if needed
#         gd_income.configure_column('Amount ($)', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
#         grid_options_income = gd_income.build()
#         AgGrid(income_df, gridOptions=grid_options_income, height=200)

#         st.write(f"**Total Income:** ${total_income:.2f}")
    
#     with col2:
#         st.write("#### Expenses")
#         gd_expense = GridOptionsBuilder.from_dataframe(expense_df)
#         gd_expense.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=5)  # Paginate if needed
#         gd_expense.configure_column('Amount ($)', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
#         grid_options_expense = gd_expense.build()
#         AgGrid(expense_df, gridOptions=grid_options_expense, height=200)

#         st.write(f"**Total Expenses:** ${total_expense:.2f}")
    
#     # Display Net Income at the bottom
#     st.success(f"**Net Income:** ${net_income:.2f}")
    