# =============================================
# forecasting_pipeline.py
# Path: notebooks/forecasting_pipeline.py
# Purpose: Generate 6-month sales forecast
# =============================================

import pandas as pd
import numpy as np
import os

GOLD = "data/gold"
os.makedirs(GOLD, exist_ok=True)

print("=" * 50)
print("  Forecasting Pipeline")
print("=" * 50)

# -----------------------------------------------
# Load Monthly Sales Trend
# -----------------------------------------------
print("\n📂 Loading monthly_sales_trend.csv...")

try:
    monthly = pd.read_csv(f"{GOLD}/monthly_sales_trend.csv")
except FileNotFoundError:
    print("❌ monthly_sales_trend.csv not found!")
    print("   Run silver_to_gold.py first.")
    exit()

print(f"   Loaded {len(monthly)} months of data")

# Sort by month
monthly = monthly.sort_values("year_month").reset_index(drop=True)

# -----------------------------------------------
# Simple Moving Average Forecast
# (No extra libraries needed — pure pandas/numpy)
# -----------------------------------------------
print("\n🔨 Generating forecast...")

# Use last 3 months average as base forecast
window = 3

# Calculate rolling average
monthly["rolling_avg"] = monthly["monthly_revenue"].rolling(window=window).mean()

# Growth rate from recent months
recent = monthly.tail(6)["monthly_revenue"]
avg_growth_rate = (recent.pct_change().mean())  # average % change per month
avg_growth_rate = max(min(avg_growth_rate, 0.15), -0.10)  # cap between -10% and +15%

print(f"   Average monthly growth rate: {avg_growth_rate*100:.2f}%")

# Last known revenue
last_revenue = monthly["monthly_revenue"].iloc[-1]
last_month   = monthly["year_month"].iloc[-1]

# Generate next 6 months
last_date = pd.to_datetime(last_month + "-01")
future_months   = []
future_forecast = []

for i in range(1, 7):
    # Next month date
    next_date    = last_date + pd.DateOffset(months=i)
    next_month   = next_date.strftime("%Y-%m")
    # Forecast = last revenue * (1 + growth)^i
    next_forecast = last_revenue * ((1 + avg_growth_rate) ** i)

    future_months.append(next_month)
    future_forecast.append(round(next_forecast, 2))

# -----------------------------------------------
# Build forecast dataframe
# -----------------------------------------------

# Historical part — actual sales
hist_df = monthly[["year_month", "monthly_revenue"]].copy()
hist_df.columns = ["year_month", "sales"]
hist_df["forecast"] = np.nan

# Future part — forecast only
future_df = pd.DataFrame({
    "year_month": future_months,
    "sales":      np.nan,
    "forecast":   future_forecast
})

# Combine
forecast_df = pd.concat([hist_df, future_df], ignore_index=True)

# Fill NaN with 0 for cleaner display
forecast_df["sales"]    = forecast_df["sales"].fillna(0)
forecast_df["forecast"] = forecast_df["forecast"].fillna(0)

forecast_df.to_csv(f"{GOLD}/sales_forecast.csv", index=False)

print(f"   ✅ sales_forecast.csv → {len(forecast_df)} rows")
print(f"\n   📈 6-Month Forecast Preview:")
print(future_df.to_string(index=False))

print("\n" + "=" * 50)
print("  ✅ Forecasting Pipeline Complete!")
print("=" * 50)