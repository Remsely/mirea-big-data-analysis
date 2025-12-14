import time

import pandas as pd
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import train_test_split

data = pd.read_csv('data/results.csv')

features = ['grid', 'constructorId', 'driverId']
target_col = 'positionOrder'

X = data[features]

y = (data[target_col] <= 10).astype(int)

print(f"Признаки: {features}")
print(f"Целевое событие: Финиш в очках (positionOrder <= 10)")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Размер обучающей выборки: {X_train.shape[0]}")
print(f"Размер тестовой выборки: {X_test.shape[0]}\n")

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

start_time = time.time()
rf_model.fit(X_train, y_train)
rf_time = time.time() - start_time

rf_pred = rf_model.predict(X_test)

rf_f1 = f1_score(y_test, rf_pred)
rf_acc = accuracy_score(y_test, rf_pred)

print(f"Время обучения Random Forest: {rf_time:.4f} сек.")
print(f"F1-score: {rf_f1:.4f}")
print(f"Accuracy: {rf_acc:.4f}\n")

cat_features = ['constructorId', 'driverId']

cb_model = CatBoostClassifier(iterations=100, random_state=42, verbose=False)

start_time = time.time()
cb_model.fit(X_train, y_train, cat_features=cat_features)
cb_time = time.time() - start_time

cb_pred = cb_model.predict(X_test)

cb_f1 = f1_score(y_test, cb_pred)
cb_acc = accuracy_score(y_test, cb_pred)

print(f"Время обучения CatBoost: {cb_time:.4f} сек.")
print(f"F1-score: {cb_f1:.4f}")
print(f"Accuracy: {cb_acc:.4f}\n")

print(f"{'Алгоритм':<20} | {'F1-score':<10} | {'Время (сек)':<10}")
print("-" * 46)
print(f"{'Random Forest':<20} | {rf_f1:.4f}     | {rf_time:.4f}")
print(f"{'CatBoost':<20} | {cb_f1:.4f}     | {cb_time:.4f}")

print("\n--- Краткий вывод ---")
if cb_f1 > rf_f1:
    print("CatBoost показал лучшее качество (F1-score).")
else:
    print("Random Forest показал лучшее качество (F1-score).")

if cb_time < rf_time:
    print("CatBoost обучился быстрее.")
else:
    print("Random Forest обучился быстрее.")
