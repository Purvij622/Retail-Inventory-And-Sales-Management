import pandas as pd

# Load Gold Layer dataset
sales_data = pd.read_csv("data/gold/sales_gold.csv")

# Total Revenue
total_revenue = sales_data["payment_value"].sum()

print("\n=== TOTAL REVENUE ===")
print(round(total_revenue, 2))

# Total Orders
total_orders = sales_data["order_id"].nunique()

print("\n=== TOTAL ORDERS ===")
print(total_orders)

# Average Order Value
average_order_value = total_revenue / total_orders

print("\n=== AVERAGE ORDER VALUE ===")
print(round(average_order_value, 2))

# Top Payment Types
payment_types = sales_data["payment_type"].value_counts()

print("\n=== PAYMENT TYPES ===")
print(payment_types)

# Top Customer States
top_states = sales_data["customer_state"].value_counts().head(10)

print("\n=== TOP CUSTOMER STATES ===")
print(top_states)