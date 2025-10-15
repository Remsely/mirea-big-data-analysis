from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)
df = housing.frame

median_house_value_series = df['MedHouseVal']

min_value = median_house_value_series.min()
max_value = median_house_value_series.max()

print(f" - Минимальное значение: {min_value}")
print(f" - Максимальное значение: {max_value}")
