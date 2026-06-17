import pandas as pd

# Load datasets
customers = pd.read_csv("data/bronze/olist_customers_dataset.csv")
orders = pd.read_csv("data/bronze/olist_orders_dataset.csv")
products = pd.read_csv("data/bronze/olist_products_dataset.csv")
payments = pd.read_csv("data/bronze/olist_order_payments_dataset.csv")
order_items = pd.read_csv("data/bronze/olist_order_items_dataset.csv")

# Print dataset shapes
print("Customers Shape:", customers.shape)
print("Orders Shape:", orders.shape)
print("Products Shape:", products.shape)
print("Payments Shape:", payments.shape)
print("Order Items Shape:", order_items.shape)

# Print columns
print("\nOrders Columns:\n")
print(orders.columns)

# Missing values check
print("\nMissing Values in Orders:\n")
print(orders.isnull().sum())