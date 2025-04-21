# Task5.py
def calculator():
    try:
        a = float(input("Введите первое число: "))
        op = input("Введите операцию (+, -, *, /): ")
        b = float(input("Введите второе число: "))
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("Деление на ноль!")
            result = a / b
        else:
            raise ValueError("Неверная операция!")
        print(f"Результат: {result}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")

calculator()