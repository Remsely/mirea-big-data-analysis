import matplotlib.pyplot as plt
import pandas as pd

insurance_df = pd.read_csv('data/insurance.csv')
numerical_features = ['age', 'bmi', 'children', 'charges']

plt.figure(figsize=(12, 8))

for i, column in enumerate(numerical_features, 1):
    plt.subplot(2, 2, i)
    plt.boxplot(insurance_df[column], vert=False)
    plt.title(f'Box-plot для "{column}"')
    plt.xlabel(column)

plt.tight_layout()
plt.show()
