import pandas as pd

# Load monthly sales trend
monthly_sales = pd.read_csv(
    "data/gold/monthly_sales_trend.csv"
)

# Rename columns
monthly_sales.columns = [   
    "year_month",
    "sales"
]

# EWMA Forecast
monthly_sales["forecast"] = monthly_sales[
    "sales"
].ewm(span=3).mean()

print("\n=== SALES FORECAST ===\n")
print(monthly_sales)

# Save forecast dataset
monthly_sales.to_csv(
    "data/gold/sales_forecast.csv",
    index=False
)

print("\nForecasting Completed Successfully!")