import logging
import sqlite3
import re
import subprocess
from datetime import datetime  # Для работы с датой
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
)
from telegram.ext import filters

# Импортируем новый модуль
from server_functions import ServerFunctions

# Токен бота
TOKEN = "YOUR_TOKEN_HERE"

# Твой Telegram ID
ADMIN_ID = "Your_ADMIN_ID_HERE"

# Путь к базе данных (для сервера)
DB_PATH = "/root/admin_bot/admin_users.db"

# Путь к PDF-инструкции
INSTRUCTION_PATH = "/root/admin_bot/resources/instruction_iphone.pdf"

# Путь к скрипту отправки ключа
SEND_KEY_SCRIPT = "/root/admin_bot/scripts/send_key.sh"

# Путь к скрипту генерации ключа
GENERATE_KEY_SCRIPT = "/root/admin_bot/scripts/generate_key.sh"

# Путь к скрипту удаления ключа
DELETE_KEY_SCRIPT = "/root/admin_bot/scripts/delete_key.sh"

# Состояния для ConversationHandler
ID_STATE, NAME_STATE, DELETE_STATE, ISSUE_KEY_STATE = range(4)

# Включаем логирование для отладки
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Функция для создания базы данных и таблицы
def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                ID TEXT PRIMARY KEY,
                Name TEXT NOT NULL,
                AddedDate TEXT
            )
        """)
        conn.commit()
        conn.close()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")


# Функция для создания главного меню
def get_main_menu():
    keyboard = [
        [
            KeyboardButton("Добавить пользователя"),
            KeyboardButton("Удалить пользователя"),
        ],
        [
            KeyboardButton("Список пользователей"),
            KeyboardButton("Выдать ключ и инструкцию"),
        ],
        [KeyboardButton("Сервер")],  # Новая кнопка
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Функция для создания подменю "Сервер"
def get_server_menu():
    keyboard = [[KeyboardButton("Активные")], [KeyboardButton("Назад")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "Доступ разрешён! Выберите действие:", reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")


# Обработчик для кнопки "Сервер"
async def server_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return
    await update.message.reply_text("Меню сервера:", reply_markup=get_server_menu())


# Обработчик для кнопки "Активные"
async def active_connections(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    # Создаём экземпляр класса ServerFunctions
    server_funcs = ServerFunctions()
    count, details = server_funcs.get_active_connections()

    # Отправляем результат
    await update.message.reply_text(
        f"Количество активных подключений: {count}\n{details}",
        reply_markup=get_server_menu(),
    )


# Обработчик для кнопки "Назад"
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return
    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())


# Начало диалога для добавления пользователя
async def add_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID (например, 001):", reply_markup=ReplyKeyboardRemove()
    )
    return ID_STATE


# Обработка введённого ID (для добавления)
async def add_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    # Проверяем, что ID состоит только из цифр
    if not re.match(r"^\d+$", user_id):
        await update.message.reply_text(
            "ID должен состоять только из цифр (например, 001). Попробуйте снова:"
        )
        return ID_STATE
    context.user_data["id"] = user_id
    await update.message.reply_text(
        "Введите номер телефона (например, +79059356661):",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NAME_STATE


# Обработка введённого номера телефона и сохранение
async def add_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = context.user_data["id"]
    user_name = update.message.text
    # Получаем текущую дату в формате YYYY-MM-DD
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Сохраняем данные в базу, включая дату
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO admin_users (ID, Name, AddedDate) VALUES (?, ?, ?)",
            (user_id, user_name, current_date),
        )
        conn.commit()
        conn.close()
        await update.message.reply_text(
            f"Пользователь с ID {user_id} добавлен в базу данных."
        )
    except sqlite3.IntegrityError:
        await update.message.reply_text(f"Пользователь с ID {user_id} уже существует.")
        await update.message.reply_text(
            "Выберите действие:", reply_markup=get_main_menu()
        )
        return ConversationHandler.END
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя с ID {user_id}: {e}")
        await update.message.reply_text(
            "Произошла ошибка при добавлении пользователя. Попробуйте снова."
        )
        await update.message.reply_text(
            "Выберите действие:", reply_markup=get_main_menu()
        )
        return ConversationHandler.END

    # Генерируем ключ для пользователя
    try:
        result = subprocess.run(
            [GENERATE_KEY_SCRIPT, user_id, user_name],
            capture_output=True,
            text=True,
            check=True,
        )
        await update.message.reply_text(
            f"Ключ для пользователя с ID {user_id} успешно сгенерирован."
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Ошибка при генерации ключа для ID {user_id}: {e}, stderr: {e.stderr}"
        )
        await update.message.reply_text(
            f"Ошибка: Не удалось сгенерировать ключ для пользователя с ID {user_id}."
        )
    except FileNotFoundError:
        logger.error(f"Скрипт {GENERATE_KEY_SCRIPT} не найден")
        await update.message.reply_text(
            "Ошибка: Скрипт генерации ключа не найден на сервере."
        )
    except Exception as e:
        logger.error(f"Ошибка при генерации ключа для ID {user_id}: {e}")
        await update.message.reply_text("Произошла ошибка при генерации ключа.")

    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END


# Начало диалога для удаления пользователя
async def delete_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID пользователя для удаления (например, 001):",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DELETE_STATE


# Обработка введённого ID (для удаления)
async def delete_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    # Проверяем, что ID состоит только из цифр
    if not re.match(r"^\d+$", user_id):
        await update.message.reply_text(
            "ID должен состоять только из цифр (например, 001). Попробуйте снова:"
        )
        return DELETE_STATE

    # Проверяем, существует ли пользователь, и удаляем его
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM admin_users WHERE ID = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            user_name = user[0]
            # Удаляем запись из базы
            cursor.execute("DELETE FROM admin_users WHERE ID = ?", (user_id,))
            conn.commit()
            await update.message.reply_text(f"Пользователь с ID {user_id} удалён.")
            # Удаляем файлы ключа
            try:
                result = subprocess.run(
                    [DELETE_KEY_SCRIPT, user_id, user_name],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                await update.message.reply_text(
                    f"Файлы ключа для пользователя с ID {user_id} удалены."
                )
            except subprocess.CalledProcessError as e:
                logger.error(
                    f"Ошибка при удалении ключа для ID {user_id}: {e}, stderr: {e.stderr}"
                )
                await update.message.reply_text(
                    f"Ошибка: Не удалось удалить файлы ключа для пользователя с ID {user_id}."
                )
            except FileNotFoundError:
                logger.error(f"Скрипт {DELETE_KEY_SCRIPT} не найден")
                await update.message.reply_text(
                    "Ошибка: Скрипт удаления ключа не найден на сервере."
                )
            except Exception as e:
                logger.error(f"Ошибка при удалении ключа для ID {user_id}: {e}")
                await update.message.reply_text("Произошла ошибка при удалении ключа.")
        else:
            await update.message.reply_text(f"Пользователь с ID {user_id} не найден.")
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя с ID {user_id}: {e}")
        await update.message.reply_text(
            "Произошла ошибка при удалении пользователя. Попробуйте снова."
        )

    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END


# Обработка отмены (если нужно прервать)
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Действие отменено.")
    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END


# Функция для отображения списка пользователей
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    # Извлекаем данные из базы
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT ID, Name, AddedDate FROM admin_users")
        users = cursor.fetchall()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при получении списка пользователей: {e}")
        await update.message.reply_text(
            "Произошла ошибка при получении списка пользователей."
        )
        return

    # Формируем сообщение
    if not users:
        await update.message.reply_text("Список пользователей пуст.")
    else:
        message = "Список пользователей:\n"
        for user in users:
            user_id, user_name, added_date = user
            message += f"ID: {user_id}, Номер: {user_name}, Добавлен: {added_date}\n"
        await update.message.reply_text(message)

    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())


# Начало диалога для выдачи ключа и инструкции
async def issue_key_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID пользователя (например, 999):", reply_markup=ReplyKeyboardRemove()
    )
    return ISSUE_KEY_STATE


# Обработка введённого ID для выдачи ключа и инструкции
async def issue_key_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.message.text
    # Проверяем, что ID состоит только из цифр
    if not re.match(r"^\d+$", user_id):
        await update.message.reply_text(
            "ID должен состоять только из цифр (например, 999). Попробуйте снова:"
        )
        return ISSUE_KEY_STATE

    # Проверяем, существует ли пользователь в базе
    user = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM admin_users WHERE ID = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при проверке пользователя с ID {user_id} в базе: {e}")
        await update.message.reply_text(
            "Произошла ошибка при проверке пользователя в базе данных."
        )
        await update.message.reply_text(
            "Выберите действие:", reply_markup=get_main_menu()
        )
        return ConversationHandler.END

    if not user:
        await update.message.reply_text(
            f"Пользователь с ID {user_id} не найден в базе данных."
        )
        await update.message.reply_text(
            "Выберите действие:", reply_markup=get_main_menu()
        )
        return ConversationHandler.END

    # Отправляем PDF-инструкцию
    try:
        with open(INSTRUCTION_PATH, "rb") as instruction_file:
            await update.message.reply_document(
                document=instruction_file,
                filename="instruction_iphone.pdf",
                caption="Инструкция по настройке OpenVPN для iPhone",
            )
    except FileNotFoundError:
        logger.error(f"Файл инструкции {INSTRUCTION_PATH} не найден")
        await update.message.reply_text("Ошибка: Файл инструкции не найден на сервере.")
    except Exception as e:
        logger.error(f"Ошибка при отправке инструкции: {e}")
        await update.message.reply_text("Произошла ошибка при отправке инструкции.")

    # Вызываем скрипт для получения пути к ключу
    try:
        result = subprocess.run(
            [SEND_KEY_SCRIPT, user_id], capture_output=True, text=True, check=True
        )
        key_path = result.stdout.strip().split("\n")[
            -1
        ]  # Последняя строка — путь к ключу
        with open(key_path, "rb") as key_file:
            await update.message.reply_document(
                document=key_file,
                filename=f"{user_id}.ovpn",
                caption=f"Ключ OpenVPN для пользователя с ID {user_id}",
            )
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Ошибка при вызове скрипта send_key.sh для ID {user_id}: {e}, stderr: {e.stderr}"
        )
        await update.message.reply_text(
            f"Ошибка: Ключ для пользователя с ID {user_id} не найден."
        )
    except FileNotFoundError:
        logger.error(f"Скрипт {SEND_KEY_SCRIPT} не найден")
        await update.message.reply_text(
            "Ошибка: Скрипт отправки ключа не найден на сервере."
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке ключа для ID {user_id}: {e}")
        await update.message.reply_text("Произошла ошибка при отправке ключа.")

    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END


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
        entry_points=[
            MessageHandler(
                filters.Text()
                & ~filters.Command()
                & filters.Regex("^Добавить пользователя$"),
                add_user_start,
            )
        ],
        states={
            ID_STATE: [
                MessageHandler(filters.Text() & ~filters.Command(), add_user_id)
            ],
            NAME_STATE: [
                MessageHandler(filters.Text() & ~filters.Command(), add_user_name)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(add_user_handler)

    # Создаём ConversationHandler для удаления пользователя
    delete_user_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Text()
                & ~filters.Command()
                & filters.Regex("^Удалить пользователя$"),
                delete_user_start,
            )
        ],
        states={
            DELETE_STATE: [
                MessageHandler(filters.Text() & ~filters.Command(), delete_user_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(delete_user_handler)

    # Создаём ConversationHandler для выдачи ключа и инструкции
    issue_key_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Text()
                & ~filters.Command()
                & filters.Regex("^Выдать ключ и инструкцию$"),
                issue_key_start,
            )
        ],
        states={
            ISSUE_KEY_STATE: [
                MessageHandler(filters.Text() & ~filters.Command(), issue_key_id)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(issue_key_handler)

    # Добавляем обработчик для кнопки "Список пользователей"
    application.add_handler(
        MessageHandler(
            filters.Text()
            & ~filters.Command()
            & filters.Regex("^Список пользователей$"),
            list_users,
        )
    )

    # Добавляем обработчики для меню "Сервер"
    application.add_handler(
        MessageHandler(
            filters.Text() & ~filters.Command() & filters.Regex("^Сервер$"), server_menu
        )
    )
    application.add_handler(
        MessageHandler(
            filters.Text() & ~filters.Command() & filters.Regex("^Активные$"),
            active_connections,
        )
    )
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex('^Назад$'), back_to_main))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()