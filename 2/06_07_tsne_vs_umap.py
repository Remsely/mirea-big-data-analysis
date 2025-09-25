import time
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.datasets import fetch_openml
import umap

print("Загрузка данных Fashion MNIST...")
X, y = fetch_openml('Fashion-MNIST', version=1, return_X_y=True, as_frame=False, parser='liac-arff', data_home='./scikit_learn_data')

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

print(f"Данные загружены. Используется полный набор данных из {X.shape[0]} объектов.")
print("Внимание: вычисления могут занять много времени!")

X_full = X / 255.0
y_full = y.astype(int)

# --- Визуализация с помощью t-SNE (4 запуска) ---
print("\n--- Запуск t-SNE ---")
perplexities = [5, 30, 50, 100]
tsne_total_start_time = time.time()

for perplexity in perplexities:
    print(f"Вычисление t-SNE с перплексией = {perplexity}...")
    start_time = time.time()

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        random_state=42,
    )

    X_tsne = tsne.fit_transform(X_full)
    end_time = time.time()
    print(f"t-SNE с перплексией = {perplexity} завершен за {end_time - start_time:.2f} секунд.")

    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y_full, cmap=plt.get_cmap("jet", 10), s=1)
    plt.title(f't-SNE с перплексией = {perplexity} (на полных данных)')
    plt.xlabel('Компонента 1')
    plt.ylabel('Компонента 2')
    handles, _ = scatter.legend_elements(num=10)
    plt.legend(handles, class_names, title="Классы")
    plt.show()

tsne_total_end_time = time.time()
tsne_duration = tsne_total_end_time - tsne_total_start_time
print(f"Общее время выполнения t-SNE: {tsne_duration:.2f} секунд")


# --- Визуализация с помощью UMAP (4 запуска) ---
print("\n--- Запуск UMAP ---")
umap_params = [
    {'n_neighbors': 5, 'min_dist': 0.1, 'desc': 'Локальная структура, плотные кластеры'},
    {'n_neighbors': 15, 'min_dist': 0.8, 'desc': 'Локальная структура, разреженные кластеры'},
    {'n_neighbors': 50, 'min_dist': 0.1, 'desc': 'Глобальная структура, плотные кластеры'},
    {'n_neighbors': 50, 'min_dist': 0.8, 'desc': 'Глобальная структура, разреженные кластеры'},
]
umap_total_start_time = time.time()

for params in umap_params:
    n_neighbors = params['n_neighbors']
    min_dist = params['min_dist']
    print(f"Вычисление UMAP с n_neighbors={n_neighbors} и min_dist={min_dist}...")
    start_time = time.time()

    reducer = umap.UMAP(
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=2,
        random_state=42
    )

    X_umap = reducer.fit_transform(X_full)
    end_time = time.time()
    print(f"UMAP с n_neighbors={n_neighbors} и min_dist={min_dist} завершен за {end_time - start_time:.2f} секунд.")

    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(X_umap[:, 0], X_umap[:, 1], c=y_full, cmap=plt.get_cmap("jet", 10), s=1)
    plt.title(f'UMAP: n_neighbors={n_neighbors}, min_dist={min_dist} ({params["desc"]}) (на полных данных)')
    plt.xlabel('Компонента 1')
    plt.ylabel('Компонента 2')
    handles, _ = scatter.legend_elements(num=10)
    plt.legend(handles, class_names, title="Классы")
    plt.show()

umap_total_end_time = time.time()
umap_duration = umap_total_end_time - umap_total_start_time
print(f"Общее время выполнения UMAP: {umap_duration:.2f} секунд")

print("\n--- Итоги производительности ---")
print(f"Время выполнения t-SNE (4 запуска): {tsne_duration:.2f} секунд")
print(f"Время выполнения UMAP (4 запуска): {umap_duration:.2f} секунд")

if umap_duration > 0 and tsne_duration > 0:
    if umap_duration < tsne_duration:
        print(f"UMAP был быстрее t-SNE в {tsne_duration / umap_duration:.2f} раз.")
    else:
        print(f"t-SNE был быстрее UMAP в {umap_duration / tsne_duration:.2f} раз.")
