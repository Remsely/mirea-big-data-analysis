import scipy.stats as st

observed_frequencies = [97, 98, 109, 95, 97, 104]
total_throws = sum(observed_frequencies)

expected_frequencies = [total_throws / 6] * 6

print(f"Наблюдаемые частоты: {observed_frequencies}")
print(f"Ожидаемые частоты: {expected_frequencies}")

print("H0: Наблюдаемое распределение соответствует равномерному (кубик 'честный').")
print("H1: Наблюдаемое распределение не соответствует равномерному.")

chi2_stat, p_value = st.chisquare(f_obs=observed_frequencies, f_exp=expected_frequencies)

print(f"\nРезультаты теста:")
print(f"  - Хи-квадрат статистика: {chi2_stat:.4f}")
print(f"  - p-value: {p_value:.4f}")

alpha = 0.05
if p_value < alpha:
    print(f"  -> Вывод: p-value ({p_value:.4f}) < {alpha}. Отвергаем H0. Распределение не является равномерным.")
else:
    print(f"  -> Вывод: p-value ({p_value:.4f}) >= {alpha}. Не можем отвергнуть H0. Нет оснований считать кубик 'нечестным'.\n")
