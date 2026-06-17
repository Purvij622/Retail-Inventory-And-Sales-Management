import pandas as pd

sales = pd.read_csv("data/gold/sales_gold.csv")

print("\nColumns:\n")
print(sales.columns)

print("\nFirst 5 Rows:\n")
print(sales.head())