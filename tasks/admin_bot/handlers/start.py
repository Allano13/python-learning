# handlers/start.py
# Обработчик команды /start

from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from menus import get_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start."""
    user_id = str(update.message.from_user.id)
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "Доступ разрешён! Выберите действие:", reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text("Доступ запрещён. Обратитесь к администратору.")
