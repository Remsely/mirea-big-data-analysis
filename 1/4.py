def sum_squares_until_sum_is_zero():
    numbers = []
    current_sum = 0

    print("Введите числа (по одному в строке).")
    print("Ввод закончится, когда сумма всех введённых чисел станет равна 0.")

    while True:
        input_str = input()
        number = float(input_str)
        numbers.append(number)
        current_sum += number

        if current_sum == 0:
            break

    sum_of_squares = sum(x ** 2 for x in numbers)
    print(f"Сумма квадратов всех введённых чисел: {sum_of_squares}")


if __name__ == "__main__":
    sum_squares_until_sum_is_zero()
