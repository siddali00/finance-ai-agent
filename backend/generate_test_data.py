"""
Script to generate sample multi-sheet Excel files for testing
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sales_data():
    """Generate sample sales data across multiple sheets"""
    
    # Create output directory
    os.makedirs("test_data", exist_ok=True)
    
    # ============================================
    # File 1: Sales Data by Quarter
    # ============================================
    print("Generating sales_data_by_quarter.xlsx...")
    
    # Q1 Sales
    dates_q1 = pd.date_range(start='2024-01-01', end='2024-03-31', freq='D')
    q1_data = {
        'Date': dates_q1,
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates_q1)),
        'Sales': np.random.randint(1000, 10000, len(dates_q1)),
        'Quantity': np.random.randint(1, 50, len(dates_q1)),
        'Branch': np.random.choice(['North', 'South', 'East', 'West'], len(dates_q1))
    }
    df_q1 = pd.DataFrame(q1_data)
    
    # Q2 Sales
    dates_q2 = pd.date_range(start='2024-04-01', end='2024-06-30', freq='D')
    q2_data = {
        'Date': dates_q2,
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates_q2)),
        'Sales': np.random.randint(1000, 10000, len(dates_q2)),
        'Quantity': np.random.randint(1, 50, len(dates_q2)),
        'Branch': np.random.choice(['North', 'South', 'East', 'West'], len(dates_q2))
    }
    df_q2 = pd.DataFrame(q2_data)
    
    # Q3 Sales
    dates_q3 = pd.date_range(start='2024-07-01', end='2024-09-30', freq='D')
    q3_data = {
        'Date': dates_q3,
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates_q3)),
        'Sales': np.random.randint(1000, 10000, len(dates_q3)),
        'Quantity': np.random.randint(1, 50, len(dates_q3)),
        'Branch': np.random.choice(['North', 'South', 'East', 'West'], len(dates_q3))
    }
    df_q3 = pd.DataFrame(q3_data)
    
    # Q4 Sales
    dates_q4 = pd.date_range(start='2024-10-01', end='2024-12-31', freq='D')
    q4_data = {
        'Date': dates_q4,
        'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], len(dates_q4)),
        'Sales': np.random.randint(1000, 10000, len(dates_q4)),
        'Quantity': np.random.randint(1, 50, len(dates_q4)),
        'Branch': np.random.choice(['North', 'South', 'East', 'West'], len(dates_q4))
    }
    df_q4 = pd.DataFrame(q4_data)
    
    # Summary sheet
    summary_data = {
        'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
        'Total_Sales': [
            df_q1['Sales'].sum(),
            df_q2['Sales'].sum(),
            df_q3['Sales'].sum(),
            df_q4['Sales'].sum()
        ],
        'Total_Quantity': [
            df_q1['Quantity'].sum(),
            df_q2['Quantity'].sum(),
            df_q3['Quantity'].sum(),
            df_q4['Quantity'].sum()
        ],
        'Average_Sales': [
            df_q1['Sales'].mean(),
            df_q2['Sales'].mean(),
            df_q3['Sales'].mean(),
            df_q4['Sales'].mean()
        ]
    }
    df_summary = pd.DataFrame(summary_data)
    
    # Write to Excel
    with pd.ExcelWriter('test_data/sales_data_by_quarter.xlsx', engine='openpyxl') as writer:
        df_q1.to_excel(writer, sheet_name='Q1_Sales', index=False)
        df_q2.to_excel(writer, sheet_name='Q2_Sales', index=False)
        df_q3.to_excel(writer, sheet_name='Q3_Sales', index=False)
        df_q4.to_excel(writer, sheet_name='Q4_Sales', index=False)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
    
    print("✓ Created sales_data_by_quarter.xlsx with 5 sheets")
    
    # ============================================
    # File 2: Financial Data (Revenue, Expenses, Profit)
    # ============================================
    print("\nGenerating financial_data.xlsx...")
    
    # Revenue sheet
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    revenue_data = {
        'Month': [m.strftime('%Y-%m') for m in months],
        'Revenue': np.random.randint(50000, 200000, len(months)),
        'Product_Sales': np.random.randint(30000, 150000, len(months)),
        'Service_Revenue': np.random.randint(10000, 80000, len(months)),
        'Other_Income': np.random.randint(5000, 30000, len(months))
    }
    df_revenue = pd.DataFrame(revenue_data)
    
    # Expenses sheet
    expense_data = {
        'Month': [m.strftime('%Y-%m') for m in months],
        'Salaries': np.random.randint(20000, 50000, len(months)),
        'Rent': np.random.randint(5000, 15000, len(months)),
        'Marketing': np.random.randint(3000, 12000, len(months)),
        'Utilities': np.random.randint(2000, 5000, len(months)),
        'Supplies': np.random.randint(1000, 4000, len(months)),
        'Other_Expenses': np.random.randint(2000, 8000, len(months))
    }
    df_expenses = pd.DataFrame(expense_data)
    
    # Profit sheet (calculated)
    profit_data = {
        'Month': df_revenue['Month'],
        'Revenue': df_revenue['Revenue'],
        'Total_Expenses': df_expenses.iloc[:, 1:].sum(axis=1),
        'Profit': df_revenue['Revenue'] - df_expenses.iloc[:, 1:].sum(axis=1),
        'Profit_Margin': ((df_revenue['Revenue'] - df_expenses.iloc[:, 1:].sum(axis=1)) / df_revenue['Revenue'] * 100).round(2)
    }
    df_profit = pd.DataFrame(profit_data)
    
    # Write to Excel
    with pd.ExcelWriter('test_data/financial_data.xlsx', engine='openpyxl') as writer:
        df_revenue.to_excel(writer, sheet_name='Revenue', index=False)
        df_expenses.to_excel(writer, sheet_name='Expenses', index=False)
        df_profit.to_excel(writer, sheet_name='Profit', index=False)
    
    print("✓ Created financial_data.xlsx with 3 sheets")
    
    # ============================================
    # File 3: Branch Performance
    # ============================================
    print("\nGenerating branch_performance.xlsx...")
    
    branches = ['North', 'South', 'East', 'West', 'Central']
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    
    # Sales by Branch
    branch_sales_data = []
    for month in months:
        for branch in branches:
            branch_sales_data.append({
                'Month': month.strftime('%Y-%m'),
                'Branch': branch,
                'Sales': np.random.randint(10000, 80000),
                'Customers': np.random.randint(50, 500),
                'Orders': np.random.randint(20, 200)
            })
    df_branch_sales = pd.DataFrame(branch_sales_data)
    
    # Employee Data
    employee_data = {
        'Branch': branches * 3,
        'Employee_ID': [f'EMP{i:03d}' for i in range(1, 16)],
        'Name': [f'Employee {i}' for i in range(1, 16)],
        'Department': np.random.choice(['Sales', 'Support', 'Management'], 15),
        'Salary': np.random.randint(40000, 120000, 15),
        'Hire_Date': pd.date_range(start='2020-01-01', end='2024-12-31', periods=15)
    }
    df_employees = pd.DataFrame(employee_data)
    
    # Branch Summary
    branch_summary = {
        'Branch': branches,
        'Total_Sales': [df_branch_sales[df_branch_sales['Branch'] == b]['Sales'].sum() for b in branches],
        'Total_Customers': [df_branch_sales[df_branch_sales['Branch'] == b]['Customers'].sum() for b in branches],
        'Employee_Count': [len(df_employees[df_employees['Branch'] == b]) for b in branches],
        'Avg_Salary': [df_employees[df_employees['Branch'] == b]['Salary'].mean() for b in branches]
    }
    df_summary = pd.DataFrame(branch_summary)
    
    # Write to Excel
    with pd.ExcelWriter('test_data/branch_performance.xlsx', engine='openpyxl') as writer:
        df_branch_sales.to_excel(writer, sheet_name='Sales_by_Branch', index=False)
        df_employees.to_excel(writer, sheet_name='Employees', index=False)
        df_summary.to_excel(writer, sheet_name='Branch_Summary', index=False)
    
    print("✓ Created branch_performance.xlsx with 3 sheets")
    
    # ============================================
    # File 4: Product Analysis
    # ============================================
    print("\nGenerating product_analysis.xlsx...")
    
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    
    # Product Sales
    product_sales_data = []
    for month in months:
        for product in products:
            product_sales_data.append({
                'Month': month.strftime('%Y-%m'),
                'Product': product,
                'Units_Sold': np.random.randint(100, 1000),
                'Revenue': np.random.randint(5000, 50000),
                'Cost': np.random.randint(2000, 20000),
                'Profit': np.random.randint(2000, 30000)
            })
    df_product_sales = pd.DataFrame(product_sales_data)
    
    # Product Details
    product_details = {
        'Product': products,
        'Category': ['Electronics', 'Furniture', 'Electronics', 'Clothing', 'Electronics'],
        'Price': [299.99, 599.99, 199.99, 89.99, 399.99],
        'Cost': [150.00, 300.00, 100.00, 40.00, 200.00],
        'Stock_Quantity': np.random.randint(50, 500, 5),
        'Supplier': ['Supplier A', 'Supplier B', 'Supplier A', 'Supplier C', 'Supplier B']
    }
    df_product_details = pd.DataFrame(product_details)
    
    # Monthly Summary
    monthly_summary = {
        'Month': [m.strftime('%Y-%m') for m in months],
        'Total_Revenue': [df_product_sales[df_product_sales['Month'] == m.strftime('%Y-%m')]['Revenue'].sum() for m in months],
        'Total_Units': [df_product_sales[df_product_sales['Month'] == m.strftime('%Y-%m')]['Units_Sold'].sum() for m in months],
        'Total_Profit': [df_product_sales[df_product_sales['Month'] == m.strftime('%Y-%m')]['Profit'].sum() for m in months]
    }
    df_monthly_summary = pd.DataFrame(monthly_summary)
    
    # Write to Excel
    with pd.ExcelWriter('test_data/product_analysis.xlsx', engine='openpyxl') as writer:
        df_product_sales.to_excel(writer, sheet_name='Product_Sales', index=False)
        df_product_details.to_excel(writer, sheet_name='Product_Details', index=False)
        df_monthly_summary.to_excel(writer, sheet_name='Monthly_Summary', index=False)
    
    print("✓ Created product_analysis.xlsx with 3 sheets")
    
    # ============================================
    # File 5: Simple Test File (2 sheets)
    # ============================================
    print("\nGenerating simple_test.xlsx...")
    
    # Sheet 1: Sales
    simple_sales = {
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Sales': np.random.randint(1000, 5000, 30),
        'Branch': np.random.choice(['A', 'B', 'C'], 30)
    }
    df_simple_sales = pd.DataFrame(simple_sales)
    
    # Sheet 2: Expenses
    simple_expenses = {
        'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'Expense': np.random.randint(500, 2000, 30),
        'Category': np.random.choice(['Rent', 'Utilities', 'Marketing'], 30)
    }
    df_simple_expenses = pd.DataFrame(simple_expenses)
    
    # Write to Excel
    with pd.ExcelWriter('test_data/simple_test.xlsx', engine='openpyxl') as writer:
        df_simple_sales.to_excel(writer, sheet_name='Sales', index=False)
        df_simple_expenses.to_excel(writer, sheet_name='Expenses', index=False)
    
    print("✓ Created simple_test.xlsx with 2 sheets")
    
    print("\n" + "="*60)
    print("All test files generated successfully!")
    print("="*60)
    print("\nGenerated files in 'test_data/' directory:")
    print("  1. sales_data_by_quarter.xlsx (5 sheets: Q1-Q4 + Summary)")
    print("  2. financial_data.xlsx (3 sheets: Revenue, Expenses, Profit)")
    print("  3. branch_performance.xlsx (3 sheets: Sales, Employees, Summary)")
    print("  4. product_analysis.xlsx (3 sheets: Sales, Details, Summary)")
    print("  5. simple_test.xlsx (2 sheets: Sales, Expenses)")
    print("\nYou can now upload these files to test the multi-sheet functionality!")


if __name__ == "__main__":
    generate_sales_data()

