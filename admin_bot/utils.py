# utils.py
# Утилитные функции: логирование и инициализация базы данных

import logging
import sqlite3

def setup_logging():
    """Настраивает логирование и возвращает логгер."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        level=logging.INFO
    )
    return logging.getLogger(__name__)

def init_db(db_path):
    """Инициализирует базу данных admin_users.db."""
    try:
        conn = sqlite3.connect(db_path)
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
        logger = setup_logging()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Ошибка при инициализации базы данных: {e}")
