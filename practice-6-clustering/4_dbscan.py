from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'f1_clustering.csv'
SCALED_COLS = [
    'win_rate_scaled', 'podium_rate_scaled', 'avg_grid_scaled', 'avg_finish_scaled', 'best_finish_scaled',
    'grid_vs_finish_scaled', 'avg_championship_position_pct_scaled', 'title_rate_scaled', 'performance_vs_team_scaled',
    'avg_team_position_scaled'
]
EPS = 1.5
MIN_SAMPLES = 5


def plot_k_distance(features, k=5):
    neighbors = NearestNeighbors(n_neighbors=k)
    neighbors.fit(features)
    distances, _ = neighbors.kneighbors(features)
    distances = np.sort(distances[:, k - 1])

    plt.figure(figsize=(8, 4))
    plt.plot(distances)
    plt.xlabel('Точки (отсортированные)')
    plt.ylabel(f'{k}-расстояние')
    plt.title(f'График k-расстояний (k={k}) для подбора eps')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('visualization/dbscan_k_distance.png')
    plt.show()


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    available_cols = [c for c in SCALED_COLS if c in data.columns]
    features = data[available_cols]

    plot_k_distance(features, k=MIN_SAMPLES)

    model = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)
    data['cluster'] = model.fit_predict(features)

    n_clusters = len(set(data['cluster'])) - (1 if -1 in data['cluster'].values else 0)
    n_noise = (data['cluster'] == -1).sum()

    print("\n" + "=" * 70)
    print("ОБЩАЯ СТАТИСТИКА (DBSCAN)")
    print("=" * 70)
    print(f"Всего гонщиков в выборке: {len(data)}")
    print(f"Параметры: eps={EPS}, min_samples={MIN_SAMPLES}")
    print(f"Количество кластеров: {n_clusters}")
    print(f"Количество шума (выбросов): {n_noise}")

    non_noise_mask = data['cluster'] != -1
    if n_clusters > 1 and non_noise_mask.sum() > 0:
        sil_score = silhouette_score(features[non_noise_mask], data.loc[non_noise_mask, 'cluster'])
        print(f"Коэффициент силуэта (без шума): {sil_score:.3f}")
    else:
        print("Силуэт не вычисляется: недостаточно кластеров.")

    print(f"\nРаспределение по кластерам (-1 = шум):")
    print(data['cluster'].value_counts().sort_index().to_string())
    print("\n" + "=" * 70)
    print("СРЕДНИЕ ХАРАКТЕРИСТИКИ ПО КЛАСТЕРАМ")
    print("=" * 70)

    analysis_cols = ['total_races', 'total_wins', 'total_titles', 'title_rate', 'win_rate',
                     'podium_rate', 'avg_championship_position_pct', 'avg_finish', 'avg_team_position']
    cluster_stats = data.groupby('cluster')[analysis_cols].mean().round(2)
    print(cluster_stats.to_string())

    display_cols = ['driverRef', 'total_races', 'total_wins', 'total_titles',
                    'title_rate', 'win_rate', 'avg_championship_position_pct', 'avg_team_position']

    for cluster_id in sorted(data['cluster'].unique()):
        cluster_data = data[data['cluster'] == cluster_id].copy()

        cluster_name = "ШУМ (выбросы)" if cluster_id == -1 else f"КЛАСТЕР {cluster_id}"

        print(f"\n{'=' * 70}")
        print(f"{cluster_name} — Гонщики ({len(cluster_data)} всего)")
        print("=" * 70)

        cluster_sorted = cluster_data.sort_values('total_wins', ascending=False)

        if len(cluster_sorted) <= 50:
            print(cluster_sorted[display_cols].to_string(index=False))
        else:
            print(f"Топ-50 по победам:")
            print(cluster_sorted.head(50)[display_cols].to_string(index=False))

    plt.figure(figsize=(8, 6))
    plt.scatter(
        data['avg_championship_position_pct'],
        data['win_rate'],
        c=data['cluster'],
        cmap='Spectral',
        alpha=0.7
    )
    plt.xlabel('Средняя позиция в чемпионате (%)')
    plt.ylabel('Процент побед (%)')
    plt.title(f'DBSCAN (eps={EPS}, min_samples={MIN_SAMPLES})\nШум (серый) = {n_noise} точек')
    plt.colorbar(label='Кластер (-1 = шум)')
    plt.tight_layout()
    plt.savefig('visualization/dbscan_clusters.png')
    plt.show()


if __name__ == '__main__':
    main()
