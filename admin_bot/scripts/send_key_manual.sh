#!/bin/bash

   # Проверка аргументов
   if [ $# -ne 2 ]; then
       echo "Usage: $0 <ID> <USER_NAME>"
       echo "Example: $0 001 Admin"
       exit 1
   fi

   ID="$1"
   USER_NAME="$2"
   FULL_NAME="ID: $ID $USER_NAME"

   # Путь к директории с клиентскими файлами
   CLIENT_DIR="/etc/openvpn/server/clients"
   CLIENT_CONF="$CLIENT_DIR/$ID.ovpn"

   # Проверка, что файл .ovpn существует
   if [ ! -f "$CLIENT_CONF" ]; then
       echo "Ошибка: Файл $CLIENT_CONF для пользователя $FULL_NAME не найден."
       exit 1
   fi

   # Проверка, что сертификаты есть в файле .ovpn
   if ! grep -q "BEGIN CERTIFICATE" "$CLIENT_CONF"; then
       echo "Ошибка: Файл $CLIENT_CONF не содержит сертификаты."
       exit 1
   fi

   # Отправка файла в Telegram-бот
   curl -F document=@"$CLIENT_CONF" https://api.telegram.org/bot8123179039:AAEbDOXzogkOnBob0J_XqZShDVuqE0y_VKM/sendDocument?chat_id=5208462139

   echo "Файл $ID.ovpn для пользователя $FULL_NAME успешно отправлен в Telegram."
