import matplotlib.pyplot as plt
import pandas as pd

insurance_df = pd.read_csv('data/insurance.csv')

numerical_features = ['age', 'bmi', 'children', 'charges']
insurance_df[numerical_features].hist(
    bins=30,
    figsize=(12, 8),
    layout=(2, 2),
    edgecolor='black'
)
plt.suptitle("Гистограммы для числовых показателей", y=1.02)
plt.show()
