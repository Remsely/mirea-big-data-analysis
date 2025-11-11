import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv('data/insurance.csv')

print("--- Данные 'insurance.csv' ---")
print(df.head())
print("\n")

print(f"--- Пропущенные значения: ---\n{df.isnull().sum()}\n")

df['sex'] = df['sex'].map({'female': 0, 'male': 1})
df['smoker'] = df['smoker'].map({'no': 0, 'yes': 1})

df = pd.get_dummies(df, columns=['region'], drop_first=True)

print("--- Данные после предобработки (текст в числа): ---")
print(df.head())
print("\n")

# --- Задание 2.1 ---
corr_matrix = df.corr()

target_corr = corr_matrix['charges'].sort_values(ascending=False)

print(target_corr)
print("\n")

most_correlated_var = target_corr.index[1]
print(f"Наиболее коррелирующая переменная (кроме самой 'charges'): '{most_correlated_var}'")

# --- Задание 2.2: Реализация регрессии вручную (Градиентный спуск) ---
X = np.array(df[most_correlated_var])
y = np.array(df['charges'])


def mserror(X, y, w1, w0):
    y_pred = w1 * X + w0
    n = len(y)
    return np.sum((y - y_pred) ** 2) / n


def gr_mserror(X, y, w1, w0):
    y_pred = w1 * X + w0
    n = len(y)

    grad_w1 = (-2 / n) * np.sum(X * (y - y_pred))
    grad_w0 = (-2 / n) * np.sum(y - y_pred)

    return grad_w1, grad_w0


w1 = 0.0
w0 = 0.0
learning_rate = 0.1
n_iterations = 10000
eps = 0.0001

for i in range(n_iterations):
    grad_w1, grad_w0 = gr_mserror(X, y, w1, w0)

    next_w1 = w1 - learning_rate * grad_w1
    next_w0 = w0 - learning_rate * grad_w0

    if abs(next_w1 - w1) < eps and abs(next_w0 - w0) < eps:
        print(f"\nАлгоритм сошелся на итерации {i}")
        break

    w1, w0 = next_w1, next_w0

final_mse = mserror(X, y, w1, w0)

print("\n--- Результаты ручной регрессии: ---")
print(f"Наклон (w1): {w1:.2f}")
print(f"Сдвиг (w0): {w0:.2f}")
print(f"MSE (среднеквадратичная ошибка): {final_mse:.2f}")
print("\n")

# --- Задание 2.3: Визуализация регрессии ---
plt.figure(figsize=(10, 6))
plt.scatter(X, y, alpha=0.3, label='Исходные данные')

X_line = np.array([0, 1])
y_line = w1 * X_line + w0

plt.plot(X_line, y_line, color='red', linewidth=3,
         label=f'Модель: y = {w1:.2f}*x + {w0:.2f}')

plt.title(f'Линейная регрессия: {most_correlated_var} vs. charges')
plt.xlabel(most_correlated_var.capitalize())
plt.ylabel('Charges (Стоимость страховки)')
plt.legend()
plt.grid(True)
plt.show()
