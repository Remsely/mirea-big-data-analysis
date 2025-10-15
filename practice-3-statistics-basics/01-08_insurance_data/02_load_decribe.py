import pandas as pd

insurance_df = pd.read_csv('data/insurance.csv')
print(insurance_df.head())
print("-" * 63)
print(insurance_df.describe())
