# admin_bot.py
# Главный файл для запуска бота

from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from config import TOKEN, DB_PATH
from utils import setup_logging, init_db
from handlers.start import start
from handlers.server_handlers import server_menu, active_connections, total_users, back_to_main
from handlers.user_handlers import add_user_handler, delete_user_handler, issue_key_handler, list_users, cancel

logger = setup_logging()

def main() -> None:
    """Запускает бота."""
    # Инициализируем базу данных
    init_db(DB_PATH)

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(add_user_handler)
    application.add_handler(delete_user_handler)
    application.add_handler(issue_key_handler)
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex("^Список пользователей$"), list_users))
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex("^Сервер$"), server_menu))
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex("^Активные$"), active_connections))
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex("^Пользователи$"), total_users))
    application.add_handler(MessageHandler(filters.Text() & ~filters.Command() & filters.Regex("^Назад$"), back_to_main))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
