import pandas as pd

# Load Gold Layer dataset
sales_data = pd.read_csv("data/gold/sales_gold.csv")

# Convert order purchase timestamp to datetime
sales_data["order_purchase_timestamp"] = pd.to_datetime(
    sales_data["order_purchase_timestamp"]
)

# Create Year-Month column
sales_data["year_month"] = sales_data[
    "order_purchase_timestamp"
].dt.to_period("M")

# Monthly Revenue
monthly_sales = sales_data.groupby(
    "year_month"
)["payment_value"].sum()

print("\n=== MONTHLY SALES TREND ===\n")
print(monthly_sales)

# Save monthly sales to gold layer
monthly_sales.to_csv(
    "data/gold/monthly_sales_trend.csv"
)

print("\nMonthly Sales Trend Created Successfully!")