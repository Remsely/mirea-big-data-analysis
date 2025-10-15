import matplotlib.pyplot as plt
import pandas as pd

insurance_df = pd.read_csv('data/insurance.csv')

for column in ['bmi', 'charges']:
    mean_val = insurance_df[column].mean()
    median_val = insurance_df[column].median()
    mode_val = insurance_df[column].mode()[0]
    std_val = insurance_df[column].std()
    range_val = insurance_df[column].max() - insurance_df[column].min()

    print(f"\nСтатистика для '{column}':")
    print(f"  - Среднее: {mean_val:.2f}")
    print(f"  - Медиана: {median_val:.2f}")
    print(f"  - Мода: {mode_val:.2f}")
    print(f"  - Стандартное отклонение: {std_val:.2f}")
    print(f"  - Размах: {range_val:.2f}")

    plt.figure(figsize=(10, 6))
    plt.hist(insurance_df[column], bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(
        mean_val,
        color='red',
        linestyle='dashed',
        linewidth=2,
        label=f'Среднее: {mean_val:.2f}'
    )
    plt.axvline(
        median_val,
        color='green',
        linestyle='solid',
        linewidth=2,
        label=f'Медиана: {median_val:.2f}'
    )
    plt.axvline(
        mode_val,
        color='yellow',
        linestyle='dotted',
        linewidth=2,
        label=f'Мода: {mode_val:.2f}'
    )
    plt.title(f'Распределение показателя "{column}"')
    plt.xlabel(column)
    plt.ylabel('Частота')
    plt.legend()
    plt.grid(True)
    plt.show()
