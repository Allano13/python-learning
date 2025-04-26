# handlers/server_handlers.py
# Обработчики для меню "Сервер"

from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from menus import get_server_menu, get_main_menu
from server_functions import ServerFunctions

async def server_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает меню 'Сервер'."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return
    await update.message.reply_text("Меню сервера:", reply_markup=get_server_menu())

async def active_connections(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает активные подключения."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    server_funcs = ServerFunctions()
    count, details = server_funcs.get_active_connections()

    await update.message.reply_text(
        f"Количество активных подключений: {count}\n{details}",
        reply_markup=get_server_menu(),
    )

async def total_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает общее количество пользователей."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return

    server_funcs = ServerFunctions()
    count, details = server_funcs.get_total_users()

    await update.message.reply_text(
        details,
        reply_markup=get_server_menu(),
    )

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Возвращает в главное меню."""
    user_id = str(update.message.from_user.id)
    if user_id != ADMIN_ID:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
        return
    await update.message.reply_text("Выберите действие:", reply_markup=get_main_menu())
