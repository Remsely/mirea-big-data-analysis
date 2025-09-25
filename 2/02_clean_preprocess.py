import pandas as pd

csv_file = "Formula1_Pitstop_Data_1950-2024_all_rounds.csv"

df = pd.read_csv(csv_file)

print("=== Информация о таблице ===")
print(df.info())
print("\n=== Первые 5 строк ===")
print(df.head())

print("\n=== Количество пропусков в каждом столбце ===")
print(df.isna().sum())

df_clean = df.dropna()

df_clean.reset_index(drop=True, inplace=True)

df_clean.to_csv("Formula1_Pitstop_Data_clean.csv", index=False)
