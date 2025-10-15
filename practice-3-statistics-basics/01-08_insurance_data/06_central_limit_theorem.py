import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

insurance_df = pd.read_csv('data/insurance.csv')
charges_data = insurance_df['charges']

num_samples = 300
sample_sizes = [5, 30, 100, 500]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Распределение выборочных средних для "charges" при разных n', fontsize=16)

axes = axes.flatten()

for i, n in enumerate(sample_sizes):
    sample_means = []
    for _ in range(num_samples):
        sample = charges_data.sample(n, replace=True)
        sample_means.append(sample.mean())

    ax = axes[i]

    counts, bins, patches = ax.hist(sample_means, bins=30, edgecolor='black',
                                    alpha=0.7, density=True, label='Выборочные средние')
    mean_of_means = np.mean(sample_means)
    std_of_means = np.std(sample_means)

    x = np.linspace(min(sample_means), max(sample_means), 100)
    normal_curve = stats.norm.pdf(x, mean_of_means, std_of_means)
    ax.plot(x, normal_curve, 'r-', linewidth=2, label='Нормальное распределение')

    ax.set_title(f'n = {n}')
    ax.set_xlabel('Среднее расходов')
    if i % 2 == 0:
        ax.set_ylabel('Плотность вероятности')
    ax.legend()
    ax.grid(True, alpha=0.3)

    print(f"\nДля n = {n}:")
    print(f"  - Среднее: {mean_of_means:.2f}")
    print(f"  - Стандартное отклонение: {std_of_means:.2f}")

plt.tight_layout()
plt.show()
