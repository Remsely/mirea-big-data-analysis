import matplotlib.pyplot as plt
import pandas as pd

data = {
    'День': ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница'],
    'Улица': [80, 98, 75, 91, 78],
    'Гараж': [100, 82, 105, 89, 102]
}

df = pd.DataFrame(data)

print("--- Исходные данные: ---")
print(df)
print("\n")

correlation = df['Улица'].corr(df['Гараж'])
abs_corr = abs(correlation)

print(f"Значение r = {correlation:.4f} (по модулю {abs_corr:.4f}).")

plt.figure(figsize=(8, 6))
plt.scatter(df['Улица'], df['Гараж'], color='crimson', marker='o')

plt.title('Диаграмма рассеяния: Уличная стоянка vs. Гараж')
plt.xlabel('Число автомобилей на уличной стоянке')
plt.ylabel('Число автомобилей в подземном гараже')

plt.grid(True)

plt.show()
