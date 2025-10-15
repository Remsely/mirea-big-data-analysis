import pandas as pd

covid_df = pd.read_csv('data/ECDCCases.csv')

missing_percentage = (covid_df.isnull().sum() / len(covid_df)) * 100
print("Процент пропущенных значений по столбцам:")
print(missing_percentage.sort_values(ascending=False))

cols_to_drop = missing_percentage.sort_values(ascending=False).head(2).index.tolist()
covid_df.drop(columns=cols_to_drop, inplace=True)
print(f"\nУдалены столбцы с наибольшим количеством пропусков: {cols_to_drop}")

for col in covid_df.columns:
    if covid_df[col].isnull().sum() > 0:
        if covid_df[col].dtype != 'object':
            median_val = covid_df[col].median()
            covid_df.loc[covid_df[col].isnull(), col] = median_val
            print(f"Пропуски в числовом столбце '{col}' заменены медианой ({median_val}).")
        else:
            covid_df.loc[covid_df[col].isnull(), col] = 'other'
            print(f"Пропуски в категориальном столбце '{col}' заменены на 'other'.")

print("\nПроверка на наличие пропусков после обработки:")
print(covid_df.isnull().sum())

covid_df.to_csv('data/ECDCCases_cleaned_missing_values.csv', index=False)
