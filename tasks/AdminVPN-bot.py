import logging
import sqlite3
import re
from datetime import datetime  # Для работы с датой
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, ContextTypes
from telegram.ext import filters

# Токен бота (замени на свой токен)
TOKEN = "7923851324:AAHtpz9b5WjTZA9-swGFKtkzKGq3qZLKFEU"

# Твой Telegram ID (замени на свой Telegram ID)
ADMIN_ID = 5208462139

# Путь к базе данных (для сервера)
DB_PATH = "/root/admin_bot/admin_users.db"

# Состояния для ConversationHandler
ID_STATE, NAME_STATE, DELETE_STATE = range(3)

# Включаем логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция для создания базы данных и таблицы
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            ID TEXT PRIMARY KEY,
            Name TEXT NOT NULL,
            AddedDate TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("База данных инициализирована")

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        keyboard = [
            [KeyboardButton("Добавить пользователя"), KeyboardButton("Удалить пользователя")],
            [KeyboardButton("Список пользователей"), KeyboardButton("Выдать ключ и инструкцию")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Доступ разрешён! Выберите действие:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")

# Начало диалога для добавления пользователя
async def add_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text("Введите ID (например, 001):", reply_markup=ReplyKeyboardRemove())
    return ID_STATE

# Обработка введённого ID (для добавления)
async def add_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    # Проверяем, что ID состоит только из цифр
    if not re.match(r'^\d+$', user_id):
        await update.message.reply_text("ID должен состоять только из цифр (например, 001). Попробуйте снова:")
        return ID_STATE
    context.user_data['id'] = user_id
    await update.message.reply_text("Введите номер телефона (например, +79059356661):", reply_markup=ReplyKeyboardRemove())
    return NAME_STATE

# Обработка введённого номера телефона и сохранение
async def add_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = context.user_data['id']
    user_name = update.message.text
    # Получаем текущую дату в формате YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Сохраняем данные в базу, включая дату
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO admin_users (ID, Name, AddedDate) VALUES (?, ?, ?)", (user_id, user_name, current_date))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"Пользователь с ID {user_id} добавлен.")
    except sqlite3.IntegrityError:
        await update.message.reply_text(f"Пользователь с ID {user_id} уже существует.")

    # Показываем меню снова
    keyboard = [
        [KeyboardButton("Добавить пользователя"), KeyboardButton("Удалить пользователя")],
        [KeyboardButton("Список пользователей"), KeyboardButton("Выдать ключ и инструкцию")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return ConversationHandler.END

# Начало диалога для удаления пользователя
async def delete_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text("Введите ID пользователя для удаления (например, 001):", reply_markup=ReplyKeyboardRemove())
    return DELETE_STATE

# Обработка введённого ID (для удаления)
async def delete_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    # Проверяем, что ID состоит только из цифр
    if not re.match(r'^\d+$', user_id):
        await update.message.reply_text("ID должен состоять только из цифр (например, 001). Попробуйте снова:")
        return DELETE_STATE

    # Проверяем, существует ли пользователь, и удаляем его
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM admin_users WHERE ID = ?", (user_id,))
    exists = cursor.fetchone()
    if exists:
        cursor.execute("DELETE FROM admin_users WHERE ID = ?", (user_id,))
        conn.commit()
        await update.message.reply_text(f"Пользователь с ID {user_id} удалён.")
    else:
        await update.message.reply_text(f"Пользователь с ID {user_id} не найден.")
    conn.close()

    # Показываем меню снова
    keyboard = [
        [KeyboardButton("Добавить пользователя"), KeyboardButton("Удалить пользователя")],
        [KeyboardButton("Список пользователей"), KeyboardButton("Выдать ключ и инструкцию")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return ConversationHandler.END

# Обработка отмены (если нужно прервать)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    keyboard = [
        [KeyboardButton("Добавить пользователя"), KeyboardButton("Удалить пользователя")],
        [KeyboardButton("Список пользователей"), KeyboardButton("Выдать ключ и инструкцию")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    return ConversationHandler.END

# Функция для отображения списка пользователей
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    # Извлекаем данные из базы
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Name, AddedDate FROM admin_users")
    users = cursor.fetchall()
    conn.close()

    # Формируем сообщение
    if not users:
        await update.message.reply_text("Список пользователей пуст.")
    else:
        message = "Список пользователей:\n"
        for user in users:
            user_id, user_name, added_date = user
            message += f"ID: {user_id}, Номер: {user_name}, Добавлен: {added_date}\n"
        await update.message.reply_text(message)

    # Показываем меню снова
    keyboard = [
        [KeyboardButton("Добавить пользователя"), KeyboardButton("Удалить пользователя")],
        [KeyboardButton("Список пользователей"), KeyboardButton("Выдать ключ и инструкцию")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)

# Главная функция
def main() -> None:
    # Инициализируем базу данных
    init_db()

    # Создаём приложение (Application)
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Создаём ConversationHandler для добавления пользователя
    add_user_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text() & ~filters.Command() & filters.Regex('^Добавить пользователя$'), add_user_start)],
        states={
            ID_STATE: [MessageHandler(filters.Text() & ~filters.Command(), add_user_id)],
            NAME_STATE: [MessageHandler(filters.Text() & ~filters.Command(), add_user_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(add_user_handler)

    # Создаём ConversationHandler для удаления пользователя
    delete_user_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Text() & ~filters.Command() & filters.Regex('^Удалить пользователя$'), delete_user_start)],
        states={
            DELETE_STATE: [MessageHandler(filters.Text() & ~filters.Command(), delete_user_id)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    application.add_handler(delete_user_handler)

    # Добавляем обработчик для кнопки "Список пользователей"
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex('^Список пользователей$'), list_users))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()


# Токен бота (замени на свой токен)
TOKEN = "7923851324:AAHtpz9b5WjTZA9-swGFKtkzKGq3qZLKFEU"

# Твой Telegram ID (замени на свой Telegram ID)
ADMIN_ID = 5208462139