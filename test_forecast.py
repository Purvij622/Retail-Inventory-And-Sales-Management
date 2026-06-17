import pandas as pd

forecast = pd.read_csv(
    "data/gold/sales_forecast.csv"
)

print(forecast.columns)

print(forecast.head())