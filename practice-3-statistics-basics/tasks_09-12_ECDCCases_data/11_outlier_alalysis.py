import pandas as pd

covid_df = pd.read_csv('data/ECDCCases_cleaned_missing_values.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print("Статистика по данным (describe()):")
print(covid_df.describe())

high_deaths_days = covid_df[covid_df['deaths'] > 3000]

print(f"\nНайдено {len(high_deaths_days)} дней, когда количество смертей превысило 3000.")
print(high_deaths_days[['dateRep', 'countriesAndTerritories', 'cases', 'deaths']])
