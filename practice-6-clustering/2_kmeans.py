from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

DATA_PATH = Path(__file__).resolve().parent / 'data' / 'f1_clustering.csv'
SCALED_COLS = [
    'win_rate_scaled', 'podium_rate_scaled', 'avg_grid_scaled', 'avg_finish_scaled', 'best_finish_scaled',
    'grid_vs_finish_scaled', 'avg_championship_position_pct_scaled', 'title_rate_scaled', 'performance_vs_team_scaled',
    'avg_team_position_scaled'
]
K_RANGE = range(2, 11)
BEST_K = 4


def main() -> None:
    data = pd.read_csv(DATA_PATH)
    available_cols = [c for c in SCALED_COLS if c in data.columns]
    features = data[available_cols]

    inertias, silhouettes = [], []
    for k in K_RANGE:
        model = KMeans(n_clusters=k, random_state=42, n_init='auto')
        labels = model.fit_predict(features)
        inertias.append(model.inertia_)
        silhouettes.append(silhouette_score(features, labels))
        print(f'k={k}: силуэт={silhouettes[-1]:.3f}')

    model = KMeans(n_clusters=BEST_K, random_state=42, n_init='auto')
    data['cluster'] = model.fit_predict(features)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(list(K_RANGE), inertias, marker='o')
    axes[0].set_xlabel('k')
    axes[0].set_ylabel('Inertia')
    axes[0].set_title('Правило локтя')

    axes[1].plot(list(K_RANGE), silhouettes, marker='o', color='green')
    axes[1].set_xlabel('k')
    axes[1].set_ylabel('Silhouette')
    axes[1].set_title('Коэффициент силуэта')
    plt.tight_layout()
    plt.savefig('visualization/kmeans_elbow.png')
    plt.show()

    print("\n" + "=" * 70)
    print("ОБЩАЯ СТАТИСТИКА")
    print("=" * 70)
    print(f"Всего гонщиков в выборке: {len(data)}")
    print(f"Количество кластеров: {BEST_K}")
    print(f"Коэффициент силуэта: {silhouettes[BEST_K - 2]:.3f}")
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


if __name__ == '__main__':
    main()
