import pandas as pd

# Load bronze datasets
customers = pd.read_csv("data/bronze/olist_customers_dataset.csv")
orders = pd.read_csv("data/bronze/olist_orders_dataset.csv")
products = pd.read_csv("data/bronze/olist_products_dataset.csv")
payments = pd.read_csv("data/bronze/olist_order_payments_dataset.csv")
order_items = pd.read_csv("data/bronze/olist_order_items_dataset.csv")

# Remove duplicates
customers = customers.drop_duplicates()
orders = orders.drop_duplicates()
products = products.drop_duplicates()
payments = payments.drop_duplicates()
order_items = order_items.drop_duplicates()

# Convert date columns
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"]
)

# Missing values check
print("\nMissing Values in Orders:\n")
print(orders.isnull().sum())

# Save cleaned datasets into silver layer
customers.to_csv("data/silver/customers_cleaned.csv", index=False)
orders.to_csv("data/silver/orders_cleaned.csv", index=False)
products.to_csv("data/silver/products_cleaned.csv", index=False)
payments.to_csv("data/silver/payments_cleaned.csv", index=False)
order_items.to_csv("data/silver/order_items_cleaned.csv", index=False)

print("\nSilver Layer Created Successfully!")