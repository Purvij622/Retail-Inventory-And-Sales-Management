# =============================================
# bronze_to_silver.py
# Path: notebooks/bronze_to_silver.py
# Purpose: Clean raw CSV files → save to silver
# =============================================

import pandas as pd
import os

# ---------- Paths ----------
BRONZE = "data/bronze"
SILVER = "data/silver"

os.makedirs(SILVER, exist_ok=True)

print("=" * 50)
print("  Bronze → Silver ETL Pipeline")
print("=" * 50)

# -----------------------------------------------
# 1. CUSTOMERS
# -----------------------------------------------
print("\n📦 Processing Customers...")
customers = pd.read_csv(f"{BRONZE}/olist_customers_dataset.csv")
print(f"   Raw rows: {len(customers)}")

customers = customers.drop_duplicates(subset=["customer_id"])
customers = customers.dropna(subset=["customer_id", "customer_state"])
customers = customers[["customer_id","customer_unique_id","customer_city","customer_state"]]

customers.to_csv(f"{SILVER}/customers_cleaned.csv", index=False)
print(f"   ✅ Cleaned rows: {len(customers)} → silver/customers_cleaned.csv")

# -----------------------------------------------
# 2. ORDERS
# -----------------------------------------------
print("\n📦 Processing Orders...")
orders = pd.read_csv(f"{BRONZE}/olist_orders_dataset.csv")
print(f"   Raw rows: {len(orders)}")

orders = orders.drop_duplicates(subset=["order_id"])
orders = orders.dropna(subset=["order_id", "customer_id"])
orders["order_status"] = orders["order_status"].fillna("delivered")

orders = orders[[
    "order_id","customer_id","order_status",
    "order_purchase_timestamp","order_delivered_customer_date"
]]
orders = orders.rename(columns={"order_delivered_customer_date": "order_delivered_timestamp"})

orders.to_csv(f"{SILVER}/orders_cleaned.csv", index=False)
print(f"   ✅ Cleaned rows: {len(orders)} → silver/orders_cleaned.csv")

# -----------------------------------------------
# 3. PAYMENTS
# -----------------------------------------------
print("\n📦 Processing Payments...")
payments = pd.read_csv(f"{BRONZE}/olist_order_payments_dataset.csv")
print(f"   Raw rows: {len(payments)}")

payments = payments.drop_duplicates()
payments = payments.dropna(subset=["order_id", "payment_value"])
payments = payments[payments["payment_value"] > 0]
payments = payments[["order_id","payment_type","payment_value"]]

payments.to_csv(f"{SILVER}/payments_cleaned.csv", index=False)
print(f"   ✅ Cleaned rows: {len(payments)} → silver/payments_cleaned.csv")

# -----------------------------------------------
# 4. PRODUCTS
# -----------------------------------------------
print("\n📦 Processing Products...")
products  = pd.read_csv(f"{BRONZE}/olist_products_dataset.csv")
cat_trans = pd.read_csv(f"{BRONZE}/product_category_name_translation.csv")
print(f"   Raw rows: {len(products)}")

products = products.drop_duplicates(subset=["product_id"])
products = products.dropna(subset=["product_id"])
products = products.merge(cat_trans, on="product_category_name", how="left")
products["product_category_name"] = products["product_category_name_english"].fillna(
    products["product_category_name"]
)
products = products[["product_id","product_category_name","product_weight_g"]]

products.to_csv(f"{SILVER}/products_cleaned.csv", index=False)
print(f"   ✅ Cleaned rows: {len(products)} → silver/products_cleaned.csv")

# -----------------------------------------------
# 5. ORDER ITEMS
# -----------------------------------------------
print("\n📦 Processing Order Items...")
order_items = pd.read_csv(f"{BRONZE}/olist_order_items_dataset.csv")
print(f"   Raw rows: {len(order_items)}")

order_items = order_items.drop_duplicates()
order_items = order_items.dropna(subset=["order_id", "product_id"])
order_items = order_items[order_items["price"] > 0]
order_items = order_items[["order_id","product_id","price","order_item_id"]]
order_items = order_items.rename(columns={"order_item_id": "quantity"})

order_items.to_csv(f"{SILVER}/order_items_cleaned.csv", index=False)
print(f"   ✅ Cleaned rows: {len(order_items)} → silver/order_items_cleaned.csv")

print("\n" + "=" * 50)
print("  ✅ Bronze → Silver Complete!")
print("=" * 50)