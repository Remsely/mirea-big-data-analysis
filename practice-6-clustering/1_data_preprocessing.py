from pathlib import Path

import pandas as pd
from sklearn.preprocessing import StandardScaler

RAW_DIR = Path(__file__).resolve().parent / 'data'
OUTPUT_PATH = RAW_DIR / 'f1_clustering.csv'

FEATURE_COLS = [
    'win_rate', 'podium_rate', 'avg_grid', 'avg_finish', 'best_finish', 'grid_vs_finish',
    'avg_championship_position_pct', 'title_rate'
]


def build_feature_table() -> pd.DataFrame:
    results = pd.read_csv(RAW_DIR / 'results.csv')
    races = pd.read_csv(RAW_DIR / 'races.csv')
    drivers = pd.read_csv(RAW_DIR / 'drivers.csv')
    driver_standings = pd.read_csv(RAW_DIR / 'driver_standings.csv')
    constructor_standings = pd.read_csv(RAW_DIR / 'constructor_standings.csv')

    year_final_race = races.groupby('year')['raceId'].max().reset_index()
    year_final_race.columns = ['year', 'final_raceId']

    team_strength = (
        constructor_standings
        .merge(year_final_race, left_on='raceId', right_on='final_raceId')
        .groupby(['constructorId', 'year'])['position']
        .min()
        .reset_index()
    )
    team_strength.columns = ['constructorId', 'year', 'team_position']

    final_standings = (
        driver_standings
        .merge(year_final_race, left_on='raceId', right_on='final_raceId')[['driverId', 'year', 'position', 'points']]
    )

    drivers_per_season = (
        final_standings
        .groupby('year')['driverId']
        .nunique()
        .reset_index()
    )
    drivers_per_season.columns = ['year', 'total_drivers']

    final_standings = final_standings.merge(drivers_per_season, on='year', how='left')

    final_standings['championship_position_pct'] = (
            (final_standings['total_drivers'] - final_standings['position']) /
            (final_standings['total_drivers'] - 1) * 100
    ).clip(0, 100)

    avg_championship = (
        final_standings
        .groupby('driverId')['championship_position_pct']
        .mean()
        .reset_index()
    )
    avg_championship.columns = ['driverId', 'avg_championship_position_pct']

    career_seasons = (
        final_standings
        .groupby('driverId')['year']
        .nunique()
        .reset_index()
    )
    career_seasons.columns = ['driverId', 'career_seasons']

    titles = (
        final_standings[final_standings['position'] == 1]
        .groupby('driverId')
        .size()
        .reset_index(name='total_titles')
    )

    merged = (
        results
        .merge(races[['raceId', 'year']], on='raceId', how='left')
        .merge(drivers[['driverId', 'driverRef', 'nationality']], on='driverId', how='left')
        .merge(team_strength, on=['constructorId', 'year'], how='left')
    )
    merged = merged[merged['positionOrder'] > 0]
    merged['team_position'] = merged['team_position'].fillna(merged['team_position'].median())

    features = (
        merged.groupby(['driverId', 'driverRef', 'nationality'])
        .agg(
            total_races=('raceId', 'nunique'),
            total_wins=('positionOrder', lambda x: (x == 1).sum()),
            total_podiums=('positionOrder', lambda x: (x <= 3).sum()),
            avg_grid=('grid', 'mean'),
            avg_finish=('positionOrder', 'mean'),
            best_finish=('positionOrder', 'min'),
            avg_team_position=('team_position', 'mean'),
        )
        .reset_index()
    )

    features = features.merge(avg_championship, on='driverId', how='left')
    features = features.merge(titles, on='driverId', how='left')
    features = features.merge(career_seasons, on='driverId', how='left')

    features['avg_championship_position_pct'] = features['avg_championship_position_pct'].fillna(0)
    features['total_titles'] = features['total_titles'].fillna(0).astype(int)
    features['career_seasons'] = features['career_seasons'].fillna(1).astype(int)
    features['win_rate'] = features['total_wins'] / features['total_races'] * 100
    features['podium_rate'] = features['total_podiums'] / features['total_races'] * 100
    features['grid_vs_finish'] = features['avg_finish'] - features['avg_grid']
    features['performance_vs_team'] = features['avg_team_position'] - features['avg_finish']
    features['title_rate'] = features['total_titles'] / features['career_seasons'] * 100

    FEATURE_COLS.append('performance_vs_team')
    FEATURE_COLS.append('avg_team_position')

    return features[features['total_races'] >= 10]


def scale_features(df: pd.DataFrame) -> pd.DataFrame:
    filled = df.copy()
    for col in FEATURE_COLS:
        if col in filled.columns:
            filled[col] = filled[col].fillna(filled[col].median())

    scaler = StandardScaler()
    cols_to_scale = [c for c in FEATURE_COLS if c in filled.columns]
    scaled = scaler.fit_transform(filled[cols_to_scale])

    scaled_df = pd.DataFrame(
        scaled,
        columns=[f'{col}_scaled' for col in cols_to_scale],
        index=filled.index,
    )
    return pd.concat([filled, scaled_df], axis=1)


def main() -> None:
    feature_df = build_feature_table()
    dataset = scale_features(feature_df)
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f'Сохранено {len(dataset)} гонщиков в {OUTPUT_PATH}')

    print("\nПример данных (топ-10 по title_rate):")
    preview_cols = ['driverRef', 'total_races', 'total_wins', 'total_titles', 'career_seasons', 'title_rate',
                    'win_rate', 'avg_championship_position_pct']
    print(dataset.nlargest(10, 'title_rate')[preview_cols].to_string(index=False))


if __name__ == '__main__':
    main()
