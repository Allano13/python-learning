# Task7: Проверка простого числа:
# Напиши функцию, которая проверяет, является ли введённое число простым.
# Запрашивай число, обрабатывай ошибки (нецелое, отрицательное, пустой ввод).
# Вывод: <число> — простое или <число> — не простое.
# Подсказка: Используй цикл for, range(), условные операторы.


def is_prime(number):
    """Алгоритм определения


    Args:
        number (int): Число для определения


    Returns:
        str: Возвращает значение в строке 'простое' или 'не простое'
    """
    if number < 2:
        return "не простое"
    for i in range(2, int(number**0.5 + 1)):
        if number % i == 0:
            return "не простое"
    else:
        return "простое"


def get_continue_choice():
    # UV для удобного цикла
    while True:
        choice = input("Проверить число? (y/n, Ctrl+C): ").lower()
        if choice in ("y", "n"):
            return True if choice == "y" else False
        print("Ошибка: введите 'y' или 'n'")


def user_input():
    # Основной цикл с проверками
    try:
        while True:
            try:
                number_input = float(input("Введите число: "))
                if number_input == 1:
                    print("Ошибка:")
                    print("Исключение из правила")
                    print("Не является 'простым' или 'не простым'")
                    continue
                if not number_input:
                    print("Ошибка: введите число")
                    continue
                if not number_input.is_integer():
                    print("Ошибка: число нецелое")
                    continue
                if number_input < 1:
                    print("Ошибка: число отрицательное")
                    continue
                return int(number_input)

            except ValueError:
                print("Ошибка: введите число")

    except KeyboardInterrupt:  # Завершение комбинацией
        print(end="\r")
        print("Программа завершена пользователем")
        exit(0)


def main():
    # Основная функция
    while get_continue_choice():
        number = user_input()
        result = is_prime(number)
        print(f"{number} — {result}")


if __name__ == "__main__":
    main()
