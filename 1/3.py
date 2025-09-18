import math

def calculator():
    num1_str = input("Введите первое число: ")
    num1 = float(num1_str)

    op = input("Введите операцию (+, -, /, //, abs, pow, **): ").strip()

    if op != 'abs':
        num2_str = input("Введите второе число: ")
        num2 = float(num2_str)
    else:
        result = abs(num1)
        print(f"Модуль числа {num1} равен {result}")
        return

    if op == '+':
        result = num1 + num2
    elif op == '-':
        result = num1 - num2
    elif op == '/':
        if num2 == 0:
            print("Ошибка: Деление на ноль невозможно.")
            return
        result = num1 / num2
    elif op == '//':
        if num2 == 0:
            print("Ошибка: Деление на ноль невозможно.")
            return
        result = num1 // num2
    elif op in ('pow', '**'):
        result = math.pow(num1, num2)
    else:
        print(f"Неизвестная операция: '{op}'.")
        return

    print(f"Результат: {num1} {op} {num2} = {result}")

if __name__ == "__main__":
    calculator()
