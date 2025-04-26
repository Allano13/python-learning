# handlers/user_handlers.py
# Обработчики для управления пользователями

import re
import subprocess
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, ContextTypes, MessageHandler, CommandHandler
from telegram.ext import filters
from config import (
    ADMIN_ID, ID_STATE, NAME_STATE, DELETE_STATE, ISSUE_KEY_STATE,
    DB_PATH, INSTRUCTION_PATH, SEND_KEY_SCRIPT, GENERATE_KEY_SCRIPT, DELETE_KEY_SCRIPT
)
from menus import get_main_menu
from database import Database
from utils import setup_logging

logger = setup_logging()

# Начало диалога для добавления пользователя
async def add_user_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начинает диалог добавления пользователя."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID (например, 001):", reply_markup=ReplyKeyboardRemove()
    )
    return ID_STATE

async def add_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает введённый ID при добавлении пользователя."""
    user_id = update.message.text
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

async def add_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет пользователя и генерирует ключ."""
    user_id = context.user_data["id"]
    user_name = update.message.text
    db = Database(DB_PATH)
    success, message = db.add_user(user_id, user_name)
    await update.message.reply_text(message)
    if not success:
        await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
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
        logger.error(f"Ошибка при генерации ключа для ID {user_id}: {e}, stderr: {e.stderr}")
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
    """Начинает диалог удаления пользователя."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID пользователя для удаления (например, 001):",
        reply_markup=ReplyKeyboardRemove(),
    )
    return DELETE_STATE

async def delete_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Удаляет пользователя и его ключ."""
    user_id = update.message.text
    if not re.match(r"^\d+$", user_id):
        await update.message.reply_text(
            "ID должен состоять только из цифр (например, 001). Попробуйте снова:"
        )
        return DELETE_STATE

    db = Database(DB_PATH)
    success, user_name, message = db.delete_user(user_id)
    await update.message.reply_text(message)
    if not success:
        await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
        return ConversationHandler.END

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
        logger.error(f"Ошибка при удалении ключа для ID {user_id}: {e}, stderr: {e.stderr}")
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

    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END

# Функция для отображения списка пользователей
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает список всех пользователей."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    db = Database(DB_PATH)
    users = db.list_users()
    if users is None:
        await update.message.reply_text("Произошла ошибка при получении списка пользователей.")
        return

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
    """Начинает диалог выдачи ключа и инструкции."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return ConversationHandler.END
    await update.message.reply_text(
        "Введите ID пользователя (например, 999):", reply_markup=ReplyKeyboardRemove()
    )
    return ISSUE_KEY_STATE

async def issue_key_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выдаёт ключ и инструкцию пользователю."""
    user_id = update.message.text
    if not re.match(r"^\d+$", user_id):
        await update.message.reply_text(
            "ID должен состоять только из цифр (например, 999). Попробуйте снова:"
        )
        return ISSUE_KEY_STATE

    db = Database(DB_PATH)
    user = db.get_user(user_id)
    if user is None:
        await update.message.reply_text(
            "Произошла ошибка при проверке пользователя в базе данных."
        )
        await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
        return ConversationHandler.END

    if not user:
        await update.message.reply_text(
            f"Пользователь с ID {user_id} не найден в базе данных."
        )
        await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
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
        key_path = result.stdout.strip().split("\n")[-1]
        with open(key_path, "rb") as key_file:
            await update.message.reply_document(
                document=key_file,
                filename=f"{user_id}.ovpn",
                caption=f"Ключ OpenVPN для пользователя с ID {user_id}",
            )
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка при вызове скрипта send_key.sh для ID {user_id}: {e}, stderr: {e.stderr}")
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

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обрабатывает отмену диалога."""
    await update.message.reply_text("Действие отменено.")
    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
    return ConversationHandler.END

# Создаём ConversationHandler'ы
add_user_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Text() & ~filters.Command() & filters.Regex("^Добавить пользователя$"),
            add_user_start,
        )
    ],
    states={
        ID_STATE: [MessageHandler(filters.Text() & ~filters.Command(), add_user_id)],
        NAME_STATE: [MessageHandler(filters.Text() & ~filters.Command(), add_user_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

delete_user_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Text() & ~filters.Command() & filters.Regex("^Удалить пользователя$"),
            delete_user_start,
        )
    ],
    states={
        DELETE_STATE: [MessageHandler(filters.Text() & ~filters.Command(), delete_user_id)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

issue_key_handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Text() & ~filters.Command() & filters.Regex("^Выдать ключ и инструкцию$"),
            issue_key_start,
        )
    ],
    states={
        ISSUE_KEY_STATE: [MessageHandler(filters.Text() & ~filters.Command(), issue_key_id)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
