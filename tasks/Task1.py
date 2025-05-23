# Задание 1: Форматированный вывод
# Напиши скрипт, который запрашивает у пользователя два числа (через input()), складывает их и выводит результат в формате:
# Число 1: <первое число>
# Число 2: <второе число>
# Сумма: <сумма>
# Используй print() с параметром sep и правильные отступы. Убедись, что ввод обрабатывается корректно (преобразуй строки в числа).

import sys

def sum_numbers(a, b):
    """Возвращает сумму двух чисел."""
    return a + b


def enter_number():
    """Запрос числа пользователя с проверкой на ошибки."""
    while True:
        try:
            number = float(input("Введите число: "))
            if abs(number) > sys.float_info.max:
                print("Ошибка: Число слишком большое.")
                continue
            if not number.is_integer():
                print("Ошибка: Введите целое число (например, 5).")
                continue

            return int(number)

        except ValueError:
            print("Ошибка: Введите корректное число (например, 5).")


# Основной код
if __name__ == "__main__":
    a = enter_number()
    b = enter_number()

    print("Число 1:", a, sep=" ")
    print("Число 2:", b, sep=" ")
    print("Сумма:", sum_numbers(a, b), sep=" ")
