from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)
df = housing.frame

filtered_data = df.loc[(df['HouseAge'] > 50) & (df['Population'] > 2500)]

print(filtered_data)
