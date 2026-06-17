# =============================================
# build_summary.py
# Path: notebooks/build_summary.py
# Purpose: Pre-calculate KPIs once → tiny summary file
#          This makes dashboard load INSTANTLY instead of
#          reading the full 19MB sales_gold.csv every time.
# =============================================

import pandas as pd
import json
import os

GOLD = "data/gold"

print("=" * 50)
print("  Building Dashboard Summary (Performance Fix)")
print("=" * 50)

# Load the big file ONCE
df = pd.read_csv(f"{GOLD}/sales_gold.csv")
print(f"Loaded sales_gold.csv: {len(df):,} rows")

# Calculate everything dashboard needs
summary = {
    "total_revenue":   float(df["payment_value"].sum()),
    "total_orders":    int(df["order_id"].nunique()),
    "total_customers": int(df["customer_id"].nunique()),
    "top_state":       df.groupby("customer_state")["payment_value"].sum().idxmax()
                        if "customer_state" in df.columns else "N/A"
}

# Save as tiny JSON file (few KB instead of 19MB)
with open(f"{GOLD}/dashboard_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"\n✅ Summary saved to data/gold/dashboard_summary.json")
print(f"   Total Revenue:   ₹{summary['total_revenue']:,.0f}")
print(f"   Total Orders:    {summary['total_orders']:,}")
print(f"   Total Customers: {summary['total_customers']:,}")
print(f"   Top State:       {summary['top_state']}")

# Also build customer segments (used in AI Insights page)
counts = df.groupby("customer_id")["order_id"].nunique().reset_index()
counts.columns = ["customer_id", "order_count"]

def seg(n):
    if n >= 5: return "VIP"
    if n >= 2: return "Regular"
    return "New"

counts["segment"] = counts["order_count"].apply(seg)
segments = counts.groupby("segment").size().reset_index(name="customer_count")
segments.to_csv(f"{GOLD}/customer_segments.csv", index=False)
print(f"   ✅ customer_segments.csv saved")

print("\n" + "=" * 50)
print("  Done! Dashboard will now load instantly.")
print("=" * 50)