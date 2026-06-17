import pandas as pd

# Load silver datasets
customers = pd.read_csv("data/silver/customers_cleaned.csv")
orders = pd.read_csv("data/silver/orders_cleaned.csv")
payments = pd.read_csv("data/silver/payments_cleaned.csv")
order_items = pd.read_csv("data/silver/order_items_cleaned.csv")
products = pd.read_csv("data/silver/products_cleaned.csv")


sales_data = pd.merge(
    orders,
    payments,
    on="order_id",
    how="inner"
)

# Merge with customers
sales_data = pd.merge(
    sales_data,
    customers,
    on="customer_id",
    how="inner"
)

# Merge with order items
sales_data = pd.merge(
    sales_data,
    order_items,
    on="order_id",
    how="inner"
)

# Save gold layer table
sales_data.to_csv(
    "data/gold/sales_gold.csv",
    index=False
)

print("Gold Layer Created Successfully!")
print("\nGold Dataset Shape:")
print(sales_data.shape)