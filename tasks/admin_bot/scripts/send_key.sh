#!/bin/bash

# Путь к ключам
KEY_PATH="/etc/openvpn/server/clients/$1.ovpn"

# Проверяем, существует ли файл ключа
if [ -f "$KEY_PATH" ]; then
    echo "Key found: $KEY_PATH"
    echo "$KEY_PATH"
    exit 0
else
    echo "Key not found for ID: $1"
    exit 1
fi
