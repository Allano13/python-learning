import logging
import sqlite3

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class ServerFunctions:
    def __init__(self):
        self.status_file = "/var/log/openvpn/openvpn-status.log"
        self.db_path = "/root/admin_bot/admin_users.db"  # Добавляем путь к базе

    def get_active_connections(self):
        """
        Читает файл статуса OpenVPN и возвращает количество активных подключений.
        Возвращает кортеж: (количество подключений, текст с деталями).
        """
        try:
            with open(self.status_file, 'r') as file:
                lines = file.readlines()

            # Считаем строки, начинающиеся с CLIENT_LIST
            active_connections = sum(1 for line in lines if line.startswith("CLIENT_LIST"))

            if active_connections == 0:
                return (active_connections, "Нет активных подключений.")

            # Формируем детали: список подключённых пользователей
            details = "Активные подключения:\n"
            for line in lines:
                if line.startswith("CLIENT_LIST"):
                    parts = line.strip().split(',')
                    common_name = parts[1]  # ID: 001 Varvara
                    virtual_ip = parts[3]   # 10.8.0.2
                    connected_since = parts[7]  # Время подключения
                    details += f"{common_name} (IP: {virtual_ip}, подключён с {connected_since})\n"

            return (active_connections, details)

        except FileNotFoundError:
            logger.error(f"Файл статуса {self.status_file} не найден")
            return (0, "Ошибка: Файл статуса OpenVPN не найден.")
        except Exception as e:
            logger.error(f"Ошибка при чтении файла статуса: {e}")
            return (0, f"Ошибка при получении активных подключений: {str(e)}")

    def get_total_users(self):
        """
        Возвращает общее количество пользователей в таблице admin_users.
        Возвращает кортеж: (количество пользователей, текст с результатом).
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM admin_users")
            total_users = cursor.fetchone()[0]
            conn.close()
            if total_users == 0:
                return (total_users, "Пользователей в базе нет.")
            return (total_users, f"Всего пользователей: {total_users}")
        except Exception as e:
            logger.error(f"Ошибка при получении количества пользователей: {e}")
            return (0, f"Ошибка при получении количества пользователей: {str(e)}")
