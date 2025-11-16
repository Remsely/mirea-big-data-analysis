import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

df = pd.read_csv('data/cleaned_f1_data.csv')

X = df.drop(columns=['podium'])
y = df['podium']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f"Размер X_train: {X_train.shape}")
print(f"Размер X_test:  {X_test.shape}")
print(f"Размер y_train: {y_train.shape}")
print(f"Размер y_test:  {y_test.shape}")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_reg = LogisticRegression(random_state=42)
svm = SVC(random_state=42)
knn = KNeighborsClassifier(n_neighbors=5)

models = {
    "Logistic Regression": log_reg,
    "Support Vector Machine (SVM)": svm,
    "K-Nearest Neighbors (KNN)": knn
}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1])
    disp.plot()

    plt.title(f'Матрица ошибок: {name}')
    plt.show()

    print(f"\nОтчет о классификации: {name}")
    print(classification_report(y_test, y_pred, target_names=['0 (Не подиум)', '1 (Подиум)']))

print("\nВсе матрицы ошибок показаны.")
