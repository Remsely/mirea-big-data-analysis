import pandas as pd

covid_df = pd.read_csv('data/ECDCCases_cleaned_missing_values.csv')

print(f"Начальный размер данных: {covid_df.shape[0]} строк.")

num_duplicates = covid_df.duplicated().sum()
print(f"Найдено дублированных строк: {num_duplicates}")

if num_duplicates > 0:
    covid_df.drop_duplicates(inplace=True)
    print("Дубликаты удалены.")
    print(f"Размер данных после удаления дубликатов: {covid_df.shape[0]} строк.")

covid_df.to_csv('data/ECDCCases_cleaned_duplicates.csv', index=False)
