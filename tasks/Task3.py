# Задание 3: Проверка четности
# Напиши скрипт, который запрашивает у пользователя число и выводит, является ли оно четным или нечетным, в формате:
# Число <число> четное
import sys  # Для проверки на крайние значения float

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


user_number = enter_number()
definition = "четное" if user_number % 2 == 0 else "нечетное"  # Проверка четности числа

print(f"Число {user_number} {definition}")
# GitHub test edit
