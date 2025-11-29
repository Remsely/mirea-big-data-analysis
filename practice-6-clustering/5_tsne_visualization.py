from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'f1_clustering.csv'
SCALED_COLS = [
    'win_rate_scaled', 'podium_rate_scaled', 'avg_grid_scaled', 'avg_finish_scaled', 'best_finish_scaled',
    'grid_vs_finish_scaled', 'avg_championship_position_pct_scaled', 'title_rate_scaled', 'performance_vs_team_scaled',
    'avg_team_position_scaled'
]
BEST_K = 4


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    available_cols = [c for c in SCALED_COLS if c in data.columns]
    features = data[available_cols]

    kmeans = KMeans(n_clusters=BEST_K, random_state=42, n_init='auto')
    data['cluster'] = kmeans.fit_predict(features)

    print("Вычисление t-SNE 2D...")
    tsne_2d = TSNE(
        n_components=2,
        random_state=42,
        init='pca',
        learning_rate='auto',
        perplexity=30
    )
    embedding_2d = tsne_2d.fit_transform(features)
    data['tsne_2d_1'] = embedding_2d[:, 0]
    data['tsne_2d_2'] = embedding_2d[:, 1]

    print("Вычисление t-SNE 3D...")
    tsne_3d = TSNE(
        n_components=3,
        random_state=42,
        init='pca',
        learning_rate='auto',
        perplexity=30
    )
    embedding_3d = tsne_3d.fit_transform(features)
    data['tsne_3d_1'] = embedding_3d[:, 0]
    data['tsne_3d_2'] = embedding_3d[:, 1]
    data['tsne_3d_3'] = embedding_3d[:, 2]

    print("\n" + "=" * 70)
    print("t-SNE ВИЗУАЛИЗАЦИЯ")
    print("=" * 70)
    print(f"Всего гонщиков: {len(data)}")
    print(f"Исходная размерность: {len(available_cols)}")
    print(f"Количество кластеров (K-Means): {BEST_K}")
    print(f"Perplexity: 30")

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        data['tsne_2d_1'],
        data['tsne_2d_2'],
        c=data['cluster'],
        cmap='tab10',
        alpha=0.7
    )
    plt.xlabel('t-SNE измерение 1')
    plt.ylabel('t-SNE измерение 2')
    plt.title('t-SNE 2D: раскраска по кластерам K-Means')
    plt.colorbar(scatter, label='Кластер')
    plt.tight_layout()
    plt.savefig('visualization/tsne_2d.png')
    plt.show()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter_3d = ax.scatter(
        data['tsne_3d_1'],
        data['tsne_3d_2'],
        data['tsne_3d_3'],
        c=data['cluster'],
        cmap='tab10',
        alpha=0.7
    )
    ax.set_xlabel('t-SNE 1')
    ax.set_ylabel('t-SNE 2')
    ax.set_zlabel('t-SNE 3')
    ax.set_title('t-SNE 3D: раскраска по кластерам K-Means')
    fig.colorbar(scatter_3d, shrink=0.5, label='Кластер')

    plt.tight_layout()
    plt.savefig('visualization/tsne_3d.png')
    plt.show()


if __name__ == '__main__':
    main()
