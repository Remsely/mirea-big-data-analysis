import pandas as pd
import scipy.stats as st

bmi_df = pd.read_csv('data/bmi.csv')

bmi_northwest = bmi_df[bmi_df['region'] == 'northwest']['bmi']
bmi_southwest = bmi_df[bmi_df['region'] == 'southwest']['bmi']

print(f"Размер выборки для Northwest: {len(bmi_northwest)}")
print(f"Размер выборки для Southwest: {len(bmi_southwest)}")

print("\n1. Проверка на нормальность (H0: распределение нормальное)")
shapiro_nw = st.shapiro(bmi_northwest)
shapiro_sw = st.shapiro(bmi_southwest)
print(f"  - Northwest: p-value = {shapiro_nw.pvalue:.4f}")
print(f"  - Southwest: p-value = {shapiro_sw.pvalue:.4f}")
if shapiro_nw.pvalue > 0.05 and shapiro_sw.pvalue > 0.05:
    print("  -> Обе выборки могут быть из нормального распределения (p > 0.05).")
else:
    print("  -> Одна или обе выборки не распределены нормально. t-тест может быть неточным.")

print("\n2. Проверка на гомогенность дисперсий (H0: дисперсии равны)")
bartlett_test = st.bartlett(bmi_northwest, bmi_southwest)
print(f"  - p-value = {bartlett_test.pvalue:.4f}")
if bartlett_test.pvalue > 0.05:
    print("  -> Дисперсии гомогенны (равны) (p > 0.05).")
    equal_var_param = True
else:
    print("  -> Дисперсии не гомогенны (не равны). Используем поправку Уэлча.")
    equal_var_param = False

print("\n3. t-критерий Стьюдента (H0: средние значения выборок равны)")
t_stat, p_value = st.ttest_ind(bmi_northwest, bmi_southwest, equal_var=equal_var_param)

print(f"  - t-статистика: {t_stat:.4f}")
print(f"  - p-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"  -> Вывод: p-value ({p_value:.4f}) < {alpha}. "
          f"Отвергаем H0. Существуют статистически значимые различия между средними ИМТ в регионах Northwest и Southwest.")
else:
    print(
        f"  -> Вывод: p-value ({p_value:.4f}) >= {alpha}. "
        f"Не можем отвергнуть H0. Статистически значимых различий между средними ИМТ не обнаружено.")
