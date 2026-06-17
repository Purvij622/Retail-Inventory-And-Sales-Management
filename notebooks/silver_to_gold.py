# =============================================
# silver_to_gold.py
# Path: notebooks/silver_to_gold.py
# Purpose: Merge silver → business metrics → gold
# =============================================

import pandas as pd
import os

SILVER = "data/silver"
GOLD   = "data/gold"

os.makedirs(GOLD, exist_ok=True)

print("=" * 50)
print("  Silver → Gold ETL Pipeline")
print("=" * 50)

# -----------------------------------------------
# Load Silver Files
# -----------------------------------------------
print("\n📂 Loading Silver files...")

customers   = pd.read_csv(f"{SILVER}/customers_cleaned.csv")
orders      = pd.read_csv(f"{SILVER}/orders_cleaned.csv")
payments    = pd.read_csv(f"{SILVER}/payments_cleaned.csv")
products    = pd.read_csv(f"{SILVER}/products_cleaned.csv")
order_items = pd.read_csv(f"{SILVER}/order_items_cleaned.csv")

print(f"   Customers:   {len(customers):,}")
print(f"   Orders:      {len(orders):,}")
print(f"   Payments:    {len(payments):,}")
print(f"   Products:    {len(products):,}")
print(f"   Order Items: {len(order_items):,}")

# -----------------------------------------------
# 1. SALES GOLD — main fact table
# -----------------------------------------------
print("\n🔨 Building sales_gold...")

# Merge: orders + payments + customers
sales = orders.merge(payments,   on="order_id",   how="inner")
sales = sales.merge(customers,   on="customer_id", how="left")

# Parse date column
sales["order_purchase_timestamp"] = pd.to_datetime(
    sales["order_purchase_timestamp"], errors="coerce"
)

# Add useful date columns
sales["year"]       = sales["order_purchase_timestamp"].dt.year
sales["month"]      = sales["order_purchase_timestamp"].dt.month
sales["year_month"] = sales["order_purchase_timestamp"].dt.strftime("%Y-%m")

# Keep only delivered orders
sales_gold = sales[sales["order_status"] == "delivered"].copy()

sales_gold.to_csv(f"{GOLD}/sales_gold.csv", index=False)
print(f"   ✅ sales_gold.csv → {len(sales_gold):,} rows")

# -----------------------------------------------
# 2. MONTHLY SALES TREND
# -----------------------------------------------
print("\n🔨 Building monthly_sales_trend...")

monthly = (
    sales_gold.groupby("year_month")
    .agg(
        monthly_revenue  = ("payment_value", "sum"),
        total_orders     = ("order_id",      "nunique"),
        total_customers  = ("customer_id",   "nunique")
    )
    .reset_index()
    .sort_values("year_month")
)

monthly.to_csv(f"{GOLD}/monthly_sales_trend.csv", index=False)
print(f"   ✅ monthly_sales_trend.csv → {len(monthly)} months")

# -----------------------------------------------
# 3. TOP STATES
# -----------------------------------------------
print("\n🔨 Building top_states...")

top_states = (
    sales_gold.groupby("customer_state")
    .agg(
        total_revenue = ("payment_value", "sum"),
        total_orders  = ("order_id",      "nunique")
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)

top_states.to_csv(f"{GOLD}/top_states.csv", index=False)
print(f"   ✅ top_states.csv → {len(top_states)} states")

print("\n" + "=" * 50)
print("  ✅ Silver → Gold Complete!")
print("=" * 50)