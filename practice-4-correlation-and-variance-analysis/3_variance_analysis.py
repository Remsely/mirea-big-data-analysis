import warnings

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import pairwise_tukeyhsd

warnings.filterwarnings('ignore')

df = pd.read_csv('data/insurance.csv')

print("--- Данные 'insurance.csv' ---")
print(df.head())
print("\n")

unique_regions = df['region'].unique()
print(f"--- Уникальные регионы в датасете: {unique_regions} ---")
print("\n")

# --- Задание 3.1 ---
print("Задание 3.1\n")
regions = df['region'].unique()
bmi_by_region = []
for region in regions:
    bmi_by_region.append(df[df['region'] == region]['bmi'])

f_stat, p_value = stats.f_oneway(*bmi_by_region)

print(f"F-статистика: {f_stat:.4f}")
print(f"P-значение: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"Вывод: P-значение ({p_value:.4f}) < {alpha}.")
    print("-> Существуют статистически значимые различия в BMI между регионами.")
else:
    print(f"Вывод: P-значение ({p_value:.4f}) > {alpha}, не можем отклонить нулевую гипотезу.")
    print("-> Статистически значимых различий в BMI между регионами не найдено.")
print("\n")

# --- Задание 3.2 ---
print("Задание 3.2\n")

model = ols('bmi ~ C(region)', data=df).fit()
anova_table = sm.stats.anova_lm(model, type=2)

print(anova_table)

# --- Задание 3.3 ---
print("Задание 3.3\n")

pairs = []
for i in range(len(regions)):
    for j in range(i + 1, len(regions)):
        pairs.append((regions[i], regions[j]))

print(f"Всего {len(pairs)} пар для сравнения.")

alpha = 0.05
bonferroni_alpha = alpha / len(pairs)
print(f"Уровень значимости (alpha): {alpha}")
print(f"Новый уровень значимости (поправка Бонферрони): {alpha} / {len(pairs)} = {bonferroni_alpha:.4f}\n")

print("Результаты t-тестов:")
for r1, r2 in pairs:
    group1 = df[df['region'] == r1]['bmi']
    group2 = df[df['region'] == r2]['bmi']

    t_stat, p_value = stats.ttest_ind(group1, group2)

    print(f"  Пара: {r1} vs {r2}")
    print(f"    P-значение: {p_value:.4f}")

    if p_value < bonferroni_alpha:
        print(f"    Вывод: ЗНАЧИМО ({p_value:.4f} < {bonferroni_alpha:.4f})")
    else:
        print(f"    Вывод: НЕ ЗНАЧИМО ({p_value:.4f} > {bonferroni_alpha:.4f})")
print("\n")

# --- Задание 3.4 ---
print("Задание 3.4\n")

tukey_result = pairwise_tukeyhsd(
    endog=df['bmi'],
    groups=df['region'],
    alpha=0.05
)

print(tukey_result)

print("Построение графика для теста Тьюки...")
tukey_result.plot_simultaneous()
plt.title("Тест Тьюки (Tukey HSD) для BMI по Регионам")
plt.show()

# --- Задание 3.5 ---
print("Задание 3.5\n")

model_2way = ols('bmi ~ C(region) + C(sex) + C(region):C(sex)', data=df).fit()
anova_table_2way = sm.stats.anova_lm(model_2way, type=2)

print(anova_table_2way)

print("\n--- Выводы по двухфакторному ANOVA: ---")
p_region = anova_table_2way.loc['C(region)', 'PR(>F)']
p_sex = anova_table_2way.loc['C(sex)', 'PR(>F)']
p_interaction = anova_table_2way.loc['C(region):C(sex)', 'PR(>F)']

if p_region < 0.05:
    print(f"1. 'region': {p_region:.4f} (< 0.05) - ЗНАЧИМО. Регион влияет на BMI.")
else:
    print(f"1. 'region': {p_region:.4f} (> 0.05) - НЕ ЗНАЧИМО.")

if p_sex < 0.05:
    print(f"2. 'sex': {p_sex:.4f} (< 0.05) - ЗНАЧИМО. Пол влияет на BMI.")
else:
    print(f"2. 'sex': {p_sex:.4f} (> 0.05) - НЕ ЗНАЧИМО.")

if p_interaction < 0.05:
    print(f"3. 'interaction': {p_interaction:.4f} (< 0.05) - ЗНАЧИМО. Эффект региона зависит от пола.")
else:
    print(f"3. 'interaction': {p_interaction:.4f} (> 0.05) - НЕ ЗНАЧИМО.")
print("\n")

# --- Задание 3.6 ---
print("Задание 3.6\n")

df['region_sex_group'] = df['region'] + '_' + df['sex']

print("--- Новые группы для теста (первые 5): ---")
print(df['region_sex_group'].head())
print("\n")

tukey_2way_result = (
    pairwise_tukeyhsd(
        endog=df['bmi'],
        groups=df['region_sex_group'],
        alpha=0.05
    )
)

print(tukey_2way_result)

print("--- Построение графика для теста Тьюки... ---")
tukey_2way_result.plot_simultaneous()
plt.title("Тест Тьюки (Tukey HSD) для BMI по (Регион + Пол)")
plt.show()
