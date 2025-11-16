import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('data/cleaned_f1_data.csv')

plt.figure(figsize=(8, 6))
sns.countplot(x='podium', data=df)
plt.title('Баланс классов (0 = Не подиум, 1 = Подиум)')
plt.xlabel('Класс')
plt.ylabel('Количество')

balance = df['podium'].value_counts(normalize=True) * 100
print("\nВыводы о балансе классов:")
print(f"Класс 0 (Не подиум): {balance[0]:.3f}%")
print(f"Класс 1 (Подиум):    {balance[1]:.3f}%")

plt.show()
