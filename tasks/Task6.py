# Task6: Конвертер температур:
# Напиши функцию для конвертации температуры (Celsius ↔ Fahrenheit).
# Запрашивай единицы (C или F) и значение.
# Обрабатывай ошибки: некорректный ввод (ValueError), пустой ввод, неверные единицы.
# Вывод: <значение>°C = <результат>°F или <значение>°F = <результат>°C.
# Подсказка: Используй if-elif, try-except ValueError, if not input_str:.


def main():
    """Основной цикл программы.

    Запрашивает у пользователя выбор действия и выполняет конвертацию температуры.
    Обрабатывает прерывание через Ctrl+C.
    """

    try:
        while True:
            continue_choice = input(
                "Конвертировать температуру? (y/n, Ctrl+C): "
            )  # Проверка хочет ли пользователь продолжить в цикле
            if not continue_choice:
                print("Ошибка: введите 'y' или 'n'.")
                continue
            if continue_choice == "y":  # основной цикл
                scale = scale_input()
                value = value_input()
                if scale == "f":
                    result = celsius_calculations(value)
                    print(f"{value:.2f}°F = {result:.2f}°C".rstrip("0").rstrip("."))
                else:
                    result = fahrenheit_calculations(value)
                    print(f"{value:.2f}°C = {result:.2f}°F".rstrip("0").rstrip("."))
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
    """Перевод Цельсий в Фаренгейт

    Args:
        number(float): Температура в Цельсиях
    Returns:
        float: температура в Фаренгейтах
    """

    return number * 1.8 + 32


def celsius_calculations(number):
    """Переводит температуру из Фаренгейтов в Цельсии.

    Args:
        number (float): Температура в Фаренгейтах.
    Returns:
        float: Температура в Цельсиях.
    """

    return (number - 32) / 1.8


def value_input():
    """Запрашивает у пользователя значение температуры.

    Returns:
        float: Введённая температура.
    Raises:
        ValueError: Если введено некорректное значение.
    """

    # цикл с проверкой на вводимое число
    while True:
        number = input("Введите температуру: ")
        if not number:
            print("Ошибка: введите число")
            continue
        try:
            return float(number)
        except ValueError:
            print("Ошибка: введите число")


def scale_input():
    """Запрашивает у пользователя шкалу температуры (F или C).

    Returns:
        str: Выбранная шкала ("f" или "c").
    """

    # Цикл с проверкой на вводимое значение
    while True:
        scale_user = input("Введите шкалу (F/C): ").lower()
        if not scale_user:
            print("Ошибка: введите правильное значение(F/C)")
            continue
        if scale_user == "f" or scale_user == "c":
            return scale_user
        else:
            print("Ошибка: введите правильное значение(F/C)")

# основное тело программы
if __name__ == "__main__":
    main()
