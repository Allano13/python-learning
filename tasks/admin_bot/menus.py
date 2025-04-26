# menus.py
# Функции для создания меню бота

from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    """Создаёт главное меню бота."""
    keyboard = [
        [
            KeyboardButton("Добавить пользователя"),
            KeyboardButton("Удалить пользователя"),
        ],
        [
            KeyboardButton("Список пользователей"),
            KeyboardButton("Выдать ключ и инструкцию"),
        ],
        [KeyboardButton("Сервер")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_server_menu():
    """Создаёт подменю 'Сервер'."""
    keyboard = [
        [KeyboardButton("Активные")],
        [KeyboardButton("Пользователи")],
        [KeyboardButton("Назад")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
