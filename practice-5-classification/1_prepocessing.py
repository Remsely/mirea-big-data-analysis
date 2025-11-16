import pandas as pd

df = pd.read_csv('data/f1_data.csv', low_memory=False)

print("\nИсходные данные (первые строки):")
print(df.head())
print(f"\nВсего записей: {len(df)}")
print("\nСтолбцы в исходном датасете:", df.columns.tolist())

rename_map = {
    'Position Order': 'position_order',
    'Grid': 'grid',
    'Laps': 'laps',
    'Team': 'team',
}

existing_rename_map = {
    old: new for old, new in rename_map.items() if old in df.columns
}

df = df[list(existing_rename_map.keys())].rename(columns=existing_rename_map)

print("\nПосле выбора нужных столбцов:")
print(df.head())
print("\nСтолбцы после переименования:", df.columns.tolist())

for col in ['position_order', 'grid', 'laps']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['position_order'])

if 'grid' in df.columns:
    df = df[df['grid'] > 0]
if 'laps' in df.columns:
    df = df[df['laps'] > 0]

feature_cols = ['grid', 'laps']

if 'team' in df.columns:
    df['team'] = df['team'].fillna('Unknown')
    team_dummies = pd.get_dummies(df['team'], prefix='team')
    df = pd.concat([df, team_dummies], axis=1)
    feature_cols += list(team_dummies.columns)

df['podium'] = (df['position_order'] <= 3).astype(int)
feature_cols.append('podium')

df_clean = df[feature_cols].dropna()

print("\nИтог после очистки и создания признаков:")
print(df_clean.head())
print(f"\nВсего записей после очистки: {len(df_clean)}")

df_clean.to_csv('data/cleaned_f1_data.csv', index=False)

print("\nДанные обработаны и сохранены в 'data/cleaned_f1_data.csv'.")
