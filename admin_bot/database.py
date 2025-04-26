# database.py
# Класс для работы с базой данных admin_users.db

import sqlite3
from datetime import datetime
from utils import setup_logging

logger = setup_logging()

class Database:
    def __init__(self, db_path):
        """Инициализирует класс с путём к базе данных."""
        self.db_path = db_path

    def add_user(self, user_id, user_name):
        """Добавляет пользователя в базу данных."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            current_date = datetime.now().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO admin_users (ID, Name, AddedDate) VALUES (?, ?, ?)",
                (user_id, user_name, current_date),
            )
            conn.commit()
            conn.close()
            return True, f"Пользователь с ID {user_id} добавлен в базу данных."
        except sqlite3.IntegrityError:
            return False, f"Пользователь с ID {user_id} уже существует."
        except Exception as e:
            logger.error(f"Ошибка при добавлении пользователя с ID {user_id}: {e}")
            return False, f"Ошибка при добавлении пользователя: {str(e)}"

    def delete_user(self, user_id):
        """Удаляет пользователя из базы данных. Возвращает имя пользователя, если он найден."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT Name FROM admin_users WHERE ID = ?", (user_id,))
            user = cursor.fetchone()
            if user:
                user_name = user[0]
                cursor.execute("DELETE FROM admin_users WHERE ID = ?", (user_id,))
                conn.commit()
                conn.close()
                return True, user_name, f"Пользователь с ID {user_id} удалён."
            else:
                conn.close()
                return False, None, f"Пользователь с ID {user_id} не найден."
        except Exception as e:
            logger.error(f"Ошибка при удалении пользователя с ID {user_id}: {e}")
            return False, None, f"Ошибка при удалении пользователя: {str(e)}"

    def list_users(self):
        """Возвращает список всех пользователей."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT ID, Name, AddedDate FROM admin_users")
            users = cursor.fetchall()
            conn.close()
            return users
        except Exception as e:
            logger.error(f"Ошибка при получении списка пользователей: {e}")
            return None

    def get_user(self, user_id):
        """Возвращает пользователя по ID."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT Name FROM admin_users WHERE ID = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            return user
        except Exception as e:
            logger.error(f"Ошибка при проверке пользователя с ID {user_id}: {e}")
            return None
