import pandas as pd

monthly = pd.read_csv(
    "data/gold/monthly_sales_trend.csv"
)

print(monthly.columns)

print(monthly.head())