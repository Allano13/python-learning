# Task7: Проверка простого числа:
# Напиши функцию, которая проверяет, является ли введённое число простым.
# Запрашивай число, обрабатывай ошибки (нецелое, отрицательное, пустой ввод).
# Вывод: <число> — простое или <число> — не простое.
# Подсказка: Используй цикл for, range(), условные операторы.


def is_prime(number):
    """Проверяет, является ли число простым.

    Args:
        number (int): Число для проверки.
    Returns:
        str: "простое" или "не простое".
    """
    if number < 2:
        return "не простое"
    for i in range(2, int(number**0.5 + 1)):
        if number % i == 0:
            return "не простое"
    else:
        return "простое"


def get_continue_choice():
    """Запрашивает у пользователя выбор продолжить или выйти.

    Обрабатывает прерывание через Ctrl+C.
    Returns:
        bool: True если продолжаем, False если выход.
    """
    try:
        while True:
            choice = input("Проверить число? (y/n, Ctrl+C): ").lower()
            if not choice:
                print("Ошибка: введите 'y' или 'n'")
                continue
            if choice in ("y", "n"):
                return True if choice == "y" else False
            print("Ошибка: введите 'y' или 'n'")
    except KeyboardInterrupt:
        print(end="\r")
        print("Программа завершена пользователем")
        exit(0)


def user_input():
    """Запрашивает у пользователя число для проверки.

    Проверяет корректность ввода.
    Returns:
        int: Введённое число.
    Raises:
        ValueError: Если введено некорректное значение.
    """
    try:
        while True:
            try:
                number = input("Введите число: ")
                if not number:
                    print("Ошибка: введите число")
                    continue
                number_input = float(number)
                if number_input > 10**9:
                    print("Большое число! Возможна задержка.")
                if not number_input.is_integer():
                    print("Ошибка: число нецелое")
                    continue
                if number_input < 1:
                    print("Ошибка: число отрицательное")
                    continue
                return int(number_input)

            except ValueError:
                print("Ошибка: введите число")

    except KeyboardInterrupt:
        print(end="\r")
        print("Программа завершена пользователем")
        exit(0)


def main():
    """Тело основной функции

    Запрашивает у пользователя действие.
    Проводит проверку,
    выводит результат
    """
    while get_continue_choice():
        number = user_input()
        result = is_prime(number)
        print(f"{number} — {result}")



if __name__ == "__main__":
    main()
