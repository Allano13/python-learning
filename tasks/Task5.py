# Сквозной проект: CLI-калькулятор (шаг 1)
# Задание для проекта:

# Создай скрипт calculator.py, который:
# Запрашивает у пользователя два числа и операцию (+, -, *, /).
# Выполняет выбранную операцию и выводит результат в формате:
# <число1> <операция> <число2> = <результат>
# Например:
# 5 + 3 = 8
# Обрабатывает ошибки ввода (нечисловые значения, деление на ноль, неверная операция).
# Используй правильные отступы, комментарии и имена переменных по PEP 8.

from Task1 import enter_number  # импорт функции ввода из задания 1


def main_loop():
    """Основной цикл"""

    try:
        while True:
            continue_choice = input("Посчитать? (y/n, Ctrl+C): ")  # запрос действия, продолжать или нет
            if continue_choice == 'y':
                num_one = enter_number()
                num_two = enter_number()
                operation = enter_operation()
                calculate(num_one, num_two, operation)
            elif continue_choice == 'n':
                break  # Выход из программы
            else:
                print("Ошибка: введите 'y' или 'n'.")

    # Обработка прерывания Ctrl+C
    except KeyboardInterrupt:
        print(end="\r")
        print("Программа завершена пользователем")
        exit(0)


def calculate(num_one, num_two, operation):
    """Цикл калькулятора"""

    try:
        if operation == "+":
            result = num_one + num_two
        elif operation == "-":
            result = num_one - num_two
        elif operation == "*":
            result = num_one * num_two
        elif operation == "/":
            if num_two == 0:
                raise ZeroDivisionError("Деление на ноль")
            result = num_one / num_two
        else:
            raise ValueError("Некорректная операция")
        print(f"{num_one} {operation} {num_two} = {int(result) if result.is_integer() else result}")  # Вывод результата
    except ValueError as e:
        print(f"Ошибка: {e}")
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")


def enter_operation():
    """Ввод операции калькулятора"""

    available_operations = ['+', '-', '*', '/']  # Доступные операции

    # цикл ввода операции
    while True:
        try:
            char = input("Введите операцию (+, -, *, /): ")
            if char not in available_operations:
                raise ValueError

            return char

        except ValueError as e:
            print("Ошибка: выберите (+, -, *, /)")


# Основной код
if __name__ == "__main__":
    main_loop()
