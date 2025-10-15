import numpy as np
import pandas as pd
import scipy.stats as st

insurance_df = pd.read_csv('data/insurance.csv')

for column in ['bmi', 'charges']:
    print(f"\nРасчет доверительных интервалов для '{column}':")

    data = insurance_df[column]

    sample_mean = np.mean(data)
    sample_std = np.std(data, ddof=1)
    n = len(data)

    se = sample_std / np.sqrt(n)

    confidence_level_95 = 0.95
    ci_95 = st.t.interval(confidence_level_95, df=n - 1, loc=sample_mean, scale=se)

    confidence_level_99 = 0.99
    ci_99 = st.t.interval(confidence_level_99, df=n - 1, loc=sample_mean, scale=se)

    print(f"  - Среднее значение выборки: {sample_mean:.2f}")
    print(f"  - 95% доверительный интервал: ({ci_95[0]:.2f}, {ci_95[1]:.2f})")
    print(f"  - 99% доверительный интервал: ({ci_99[0]:.2f}, {ci_99[1]:.2f})")
