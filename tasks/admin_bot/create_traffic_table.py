import sqlite3
from datetime import datetime

# Подключаемся к базе данных
conn = sqlite3.connect('/root/admin_bot/admin_users.db')
cursor = conn.cursor()

# Создаём таблицу traffic_logs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS traffic_logs (
        UserID TEXT,
        SessionID TEXT,
        Date TEXT,
        BytesReceived INTEGER,
        BytesSent INTEGER,
        IsDisconnected INTEGER DEFAULT 0
    )
''')

# Создаём индекс на поле Date для быстрого поиска
cursor.execute('CREATE INDEX IF NOT EXISTS idx_traffic_logs_date ON traffic_logs (Date)')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Таблица traffic_logs создана")
