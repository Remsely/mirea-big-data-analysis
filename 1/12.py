import pandas as pd
from sklearn.datasets import fetch_california_housing

housing = fetch_california_housing(as_frame=True)
df = housing.frame

mean_values = df.apply(pd.Series.mean)

for feature_name, mean_value in mean_values.items():
    print(f"{feature_name}: {mean_value:.4f}")
