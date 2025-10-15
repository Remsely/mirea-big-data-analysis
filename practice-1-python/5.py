def main():
    n = int(input("Введите неотрицательное целое число N: "))

    if n == 0:
        print()
        return

    sequence = []
    current_number = 1

    while len(sequence) < n:
        for _ in range(current_number):
            sequence.append(current_number)
            if len(sequence) == n:
                break
        current_number += 1

    print(*sequence)


if __name__ == "__main__":
    main()
