import math


def calculate_triangle_area(a, b, c):
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area


def calculate_rectangle_area(length, width):
    return length * width


def calculate_circle_area(radius):
    return math.pi * (radius ** 2)


def main():
    shape = input("Введите название фигуры (треугольник, прямоугольник, круг): ").lower()

    result = {}

    if shape == "треугольник":
        a = float(input("Введите длину стороны a: "))
        b = float(input("Введите длину стороны b: "))
        c = float(input("Введите длину стороны c: "))
        area = calculate_triangle_area(a, b, c)
        result[shape] = area

    elif shape == "прямоугольник":
        length = float(input("Введите длину: "))
        width = float(input("Введите ширину: "))
        area = calculate_rectangle_area(length, width)
        result[shape] = area

    elif shape == "круг":
        radius = float(input("Введите радиус: "))
        area = calculate_circle_area(radius)
        result[shape] = area

    else:
        print("Неизвестная фигура. Пожалуйста, выберите из списка: треугольник, прямоугольник, круг.")
        return

    if result:
        print(result)


if __name__ == "__main__":
    main()