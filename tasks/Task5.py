# Task5.py
def calculator():
    history = []  # Список для хранения истории операций
    while True:
        try:
            a = float(input("Введите первое число (или 'q' для выхода): "))
        except ValueError:
            if a == 'q':
                break
            print("Ошибка: Введите число!")
            continue
        op = input("Введите операцию (+, -, *, /, 'h' для истории): ")
        if op == 'h':
            print("История операций:")
            for entry in history:
                print(entry)
            continue
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
        operation = f"{a} {op} {b} = {result}"
        history.append(operation)  # Добавляем операцию в историю
        print(f"Результат: {result}")
    print("Калькулятор завершен.")

calculator()