import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st

insurance_df = pd.read_csv('data/insurance.csv')

for column in ['bmi', 'charges']:
    print(f"\n--- Проверка для признака '{column}' ---")
    data = insurance_df[column]

    print("Гипотезы:")
    print("  - H0 (Нулевая гипотеза): Распределение признака не отличается от нормального.")
    print("  - H1 (Альтернативная гипотеза): Распределение признака отличается от нормального.")

    data_standardized = (data - np.mean(data)) / np.std(data)
    ks_statistic, ks_pvalue = st.kstest(data_standardized, 'norm')

    print(f"\nРезультаты KS-теста:")
    print(f"  - Статистика: {ks_statistic:.4f}")
    print(f"  - p-value: {ks_pvalue:.4f}")

    alpha = 0.05
    if ks_pvalue < alpha:
        print(f"  - Вывод: p-value ({ks_pvalue:.4f}) < {alpha}. Отвергаем H0. "
              "Распределение не является нормальным.")
    else:
        print(f"  - Вывод: p-value ({ks_pvalue:.4f}) >= {alpha}. Не можем отвергнуть H0. "
              "Распределение может быть нормальным.")

    plt.figure(figsize=(8, 6))
    st.probplot(data, dist="norm", plot=plt)
    ax = plt.gca()
    ax.get_lines()[0].set_markersize(2)

    plt.title(f'Q-Q plot для "{column}"')
    plt.grid(True, alpha=0.3)
    plt.show()
