# Task6: Конвертер температур:
# Напиши функцию для конвертации температуры (Celsius ↔ Fahrenheit).
# Запрашивай единицы (C или F) и значение.
# Обрабатывай ошибки: некорректный ввод (ValueError), пустой ввод, неверные единицы.
# Вывод: <значение>°C = <результат>°F или <значение>°F = <результат>°C.
# Подсказка: Используй if-elif, try-except ValueError, if not input_str:.


def main():
    """Цикл основной функции"""

    try:
        while True:
            continue_choice = input(
                "Конвертировать температуру? (y/n, Ctrl+C): "
            )  # Проверка хочет ли пользователь продолжить в цикле
            if continue_choice == "y":  # основной цикл
                scale = scale_input()
                value = value_input()
                if scale == "f":
                    result = celsius_calculations(value)
                    print(f"{round(value, 2)}°F = {round(result, 2)}°C")  # Вывод 1
                else:
                    result = fahrenheit_calculations(value)
                    print(f"{round(value, 2)}°C = {round(result, 2)}°F")  # Вывод 2
            elif continue_choice == "n":  # Выход из программы
                print("Завершение программы")
                break
            else:
                print("Ошибка: введите 'y' или 'n'.")

    except KeyboardInterrupt:  # Завершение комбинацией
        print(end="\r")
        print("Программа завершена пользователем")
        exit(0)


def fahrenheit_calculations(number):
    """Перевод Цельсий в Фаренгейт"""

    return number * 1.8 + 32


def celsius_calculations(number):
    """Перевод Фаренгейт в Цельсий"""

    return (number - 32) / 1.8


def value_input():
    """Ввод пользовательского значения температуры"""

    # цикл с проверкой на вводимое число
    while True:
        try:
            number = float(input("Введите температуру: "))
            return int(number)

        except ValueError:
            print("Ошибка: введите число")


def scale_input():
    """Ввод пользовательского значения шкалы"""

    # Цикл с проверкой на вводимое значение
    while True:
        scale_user = input("Введите шкалу (F/C): ").lower()
        if scale_user == "f" or scale_user == "c":
            return scale_user
        else:
            print("Ошибка: введите правильное значение(F/C)")


# основное тело программы
if __name__ == "__main__":
    main()
