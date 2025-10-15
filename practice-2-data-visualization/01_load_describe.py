import pandas as pd

csv_file = "Formula1_Pitstop_Data_1950-2024_all_rounds.csv"

df = pd.read_csv(csv_file)

print("=== Информация о таблице ===")
print(df.info())

print("\n=== Первые 5 строк ===")
print(df.head())

print("\n=== Пропуски по столбцам ===")
print(df.isna().sum())
