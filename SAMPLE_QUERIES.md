# Sample Queries for Test Data

This document contains sample queries you can use to test the Finance AI Agent with the test data files located in `backend/test_data/`.

## Test Data Files

The following test files are available:
- `branch_performance.xlsx` - Branch sales, employees, and summary data
- `financial_data.xlsx` - Revenue, expenses, and profit data by month
- `product_analysis.xlsx` - Product sales, details, and monthly summaries
- `sales_data_by_quarter.xlsx` - Quarterly sales data (Q1-Q4) with summary

## Data Analysis Queries

### Financial Data Queries

1. **Which month had the highest revenue?**
2. **What is the total revenue for the year?**
3. **What is the average profit margin?**
4. **Which month had the lowest expenses?**
5. **What is the total profit for all months?**
6. **Show me the revenue for each month**
7. **What is the average monthly revenue?**
8. **Which month had the highest profit?**
9. **What are the total expenses for the year?**
10. **Calculate the profit margin for each month**

### Branch Performance Queries

1. **Which branch had the highest total sales?**
2. **What is the average salary across all branches?**
3. **How many employees are in each branch?**
4. **Which branch has the most customers?**
5. **What is the total sales for the North branch?**
6. **Show me the sales for each branch by month**
7. **Which branch has the highest average salary?**
8. **What is the total number of orders per branch?**
9. **Which branch has the most employees?**
10. **Calculate the average sales per branch**

### Product Analysis Queries

1. **Which product had the highest revenue?**
2. **What is the total units sold for Product A?**
3. **Which product has the highest profit?**
4. **What is the average price of all products?**
5. **Show me the revenue for each product**
6. **Which product has the lowest stock quantity?**
7. **What is the total profit for all products?**
8. **Which category has the most products?**
9. **What is the average profit margin per product?**
10. **Show me products with stock quantity below 200**

### Sales by Quarter Queries

1. **Which quarter had the highest total sales?**
2. **What is the total sales for Q3?**
3. **Which product sold the most in Q4?**
4. **What is the average sales per quarter?**
5. **Which branch had the highest sales in Q2?**
6. **Show me the total quantity sold per quarter**
7. **What is the total sales for Product B across all quarters?**
8. **Which quarter had the most orders?**
9. **Calculate the average sales per day for each quarter**
10. **Which branch performed best in Q1?**

### Cross-Sheet Queries (Multiple Files)

1. **Compare revenue from financial_data with product sales**
2. **Which branch has the highest sales across all data?**
3. **What is the correlation between product sales and branch performance?**
4. **Show me total revenue from all sources**

## Visualization Queries

### Financial Data Visualizations

1. **Show me a bar chart of revenue by month**
2. **Create a line graph showing profit over time**
3. **Visualize expenses by category as a pie chart**
4. **Show me a bar chart comparing revenue and expenses**
5. **Create a line chart of profit margin over time**
6. **Visualize monthly revenue trends**
7. **Show me a stacked bar chart of revenue components**
8. **Create a chart showing profit vs expenses**

### Branch Performance Visualizations

1. **Show me a bar chart of sales by branch**
2. **Create a pie chart of total sales distribution by branch**
3. **Visualize monthly sales trends for each branch**
4. **Show me a bar chart comparing employee count by branch**
5. **Create a line chart of sales over time for each branch**
6. **Visualize average salary by branch**
7. **Show me a chart of customers per branch**
8. **Create a bar chart of total orders by branch**

### Product Analysis Visualizations

1. **Show me a bar chart of revenue by product**
2. **Create a pie chart of units sold by product**
3. **Visualize profit by product as a bar chart**
4. **Show me a line chart of product sales over time**
5. **Create a bar chart comparing revenue and profit for each product**
6. **Visualize stock quantity by product**
7. **Show me a chart of products by category**
8. **Create a line chart showing monthly revenue trends**

### Sales by Quarter Visualizations

1. **Show me a bar chart of total sales by quarter**
2. **Create a line chart of sales trends across quarters**
3. **Visualize sales by product for each quarter**
4. **Show me a bar chart comparing Q1, Q2, Q3, and Q4 sales**
5. **Create a pie chart of sales distribution by quarter**
6. **Visualize sales by branch for each quarter**
7. **Show me a stacked bar chart of product sales per quarter**
8. **Create a chart showing quantity sold by quarter**

### Advanced Visualizations

1. **Show me a comparison chart of revenue vs expenses over time**
2. **Create a dashboard showing branch performance metrics**
3. **Visualize product sales trends across all quarters**
4. **Show me a comprehensive chart of all financial metrics**
5. **Create a multi-series line chart comparing different branches**

## Tips for Testing

- Upload multiple files at once to test multi-file functionality
- Try queries that require data from multiple sheets
- Test both simple questions and complex analytical queries
- Experiment with different visualization types
- Try conversational queries like greetings to test the AI's response handling

## Example Workflow

1. Upload `financial_data.xlsx`, `branch_performance.xlsx`, and `product_analysis.xlsx`
2. Ask: "Which month had the highest profit?"
3. Ask: "Show me a bar chart of revenue by month"
4. Ask: "Which branch had the highest sales?"
5. Ask: "Create a pie chart of sales by branch"
6. Ask: "What is the total revenue for Product A?"

