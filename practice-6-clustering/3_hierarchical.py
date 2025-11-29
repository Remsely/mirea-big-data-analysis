from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'f1_clustering.csv'
SCALED_COLS = [
    'win_rate_scaled', 'podium_rate_scaled', 'avg_grid_scaled', 'avg_finish_scaled', 'best_finish_scaled',
    'grid_vs_finish_scaled', 'avg_championship_position_pct_scaled', 'title_rate_scaled', 'performance_vs_team_scaled',
    'avg_team_position_scaled'
]
N_CLUSTERS = 4


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    available_cols = [c for c in SCALED_COLS if c in data.columns]
    features = data[available_cols]

    linkage_matrix = linkage(features, method='ward')
    plt.figure(figsize=(12, 5))
    dendrogram(linkage_matrix, truncate_mode='lastp', p=40)
    plt.title('Дендрограмма (метод Ward)')
    plt.xlabel('Объекты')
    plt.ylabel('Расстояние')
    plt.tight_layout()
    plt.savefig('visualization/hierarchical_dendrogram.png')
    plt.show()

    model = AgglomerativeClustering(n_clusters=N_CLUSTERS, linkage='ward')
    data['cluster'] = model.fit_predict(features)

    sil_score = silhouette_score(features, data['cluster'])

    print("\n" + "=" * 70)
    print("ОБЩАЯ СТАТИСТИКА (Иерархическая кластеризация)")
    print("=" * 70)
    print(f"Всего гонщиков в выборке: {len(data)}")
    print(f"Количество кластеров: {N_CLUSTERS}")
    print(f"Метод связи: Ward")
    print(f"Коэффициент силуэта: {sil_score:.3f}")
    print(f"\nРаспределение по кластерам:")
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

        print(f"\n{'=' * 70}")
        print(f"КЛАСТЕР {cluster_id} — Гонщики ({len(cluster_data)} всего)")
        print("=" * 70)

        cluster_sorted = cluster_data.sort_values('total_wins', ascending=False)

        if len(cluster_sorted) <= 50:
            print(cluster_sorted[display_cols].to_string(index=False))
        else:
            print(f"Топ-50 по победам:")
            print(cluster_sorted.head(50)[display_cols].to_string(index=False))

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        data['avg_championship_position_pct'],
        data['win_rate'],
        c=data['cluster'],
        cmap='tab10',
        alpha=0.7
    )
    plt.xlabel('Средняя позиция в чемпионате (%)')
    plt.ylabel('Процент побед (%)')
    plt.title('Иерархическая кластеризация (Ward)')
    plt.colorbar(scatter, label='Кластер')
    plt.tight_layout()
    plt.savefig('visualization/hierarchical_clusters.png')
    plt.show()


if __name__ == '__main__':
    main()
