#!/bin/bash

# Путь к базе данных
DB_PATH="/root/admin_bot/admin_users.db"

# Текущая дата
CURRENT_DATE="2025-04-24"

# Извлекаем ID и номер телефона из файлов .crt
ls /etc/openvpn/server/clients/*.crt 2>/dev/null | grep "ID:" | awk -F'ID: |[.]' '{print $2}' | awk '{print $1 " " $2}' | while read id phone; do
    if [ -n "$id" ] && [ -n "$phone" ]; then
        echo "Добавляем пользователя: ID=$id, Номер=$phone"
        sqlite3 "$DB_PATH" "INSERT OR IGNORE INTO admin_users (ID, Name, AddedDate) VALUES ('$id', '$phone', '$CURRENT_DATE');"
    fi
done

echo "Добавление завершено."
