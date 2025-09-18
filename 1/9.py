from sklearn.datasets import fetch_california_housing


def check_missing_values_california_housing():
    california_housing = fetch_california_housing(as_frame=True)
    df = california_housing.frame
    print("Проверка на пропущенные значения в каждом столбце:")
    missing_values_count = df.isna().sum()
    print(missing_values_count)


if __name__ == "__main__":
    check_missing_values_california_housing()
