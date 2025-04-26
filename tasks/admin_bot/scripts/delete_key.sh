#!/bin/bash

# Проверка аргументов
if [ $# -ne 2 ]; then
    echo "Usage: $0 <ID> <USER_NAME>"
    echo "Example: $0 001 Varvara"
    exit 1
fi

ID="$1"
USER_NAME="$2"
FULL_NAME="ID: $ID $USER_NAME"

# Путь к директориям
CLIENT_DIR="/etc/openvpn/server/clients"
EASYRSA_DIR="/etc/openvpn/easy-rsa"
STATUS_FILE="/var/log/openvpn/openvpn-status.log"
IPTABLES_LOG="/root/blocked_ips.log"

# Проверка, что easy-rsa существует
if [ ! -d "$EASYRSA_DIR" ]; then
    echo "Error: Directory $EASYRSA_DIR not found."
    exit 1
fi

# Переходим в easy-rsa
cd "$EASYRSA_DIR"

# Проверяем, существует ли сертификат
if [ ! -f "pki/issued/$FULL_NAME.crt" ]; then
    echo "User with name $FULL_NAME not found."
    exit 1
fi

# Отзыв сертификата
echo "yes" | ./easyrsa revoke "$FULL_NAME"
if [ $? -ne 0 ]; then
    echo "Error: Failed to revoke certificate for $FULL_NAME."
    exit 1
fi

# Генерируем новый CRL
./easyrsa gen-crl
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate CRL."
    exit 1
fi

# Копируем обновлённый CRL в директорию OpenVPN
cp pki/crl.pem /etc/openvpn/server/

# Находим виртуальный IP-адрес пользователя из файла статуса
VIRTUAL_IP=$(grep "$FULL_NAME" "$STATUS_FILE" | grep "CLIENT_LIST" | awk -F',' '{print $4}')
if [ -n "$VIRTUAL_IP" ]; then
    echo "Found virtual IP for $FULL_NAME: $VIRTUAL_IP"
    # Блокируем IP с помощью iptables, чтобы разорвать соединение
    iptables -A INPUT -s "$VIRTUAL_IP" -j DROP
    iptables -A OUTPUT -d "$VIRTUAL_IP" -j DROP
    echo "Connection for $FULL_NAME terminated by blocking IP $VIRTUAL_IP."
    # Логируем заблокированный IP
    echo "$(date): Blocked IP $VIRTUAL_IP for user $FULL_NAME" >> "$IPTABLES_LOG"
else
    echo "User $FULL_NAME is not currently connected."
fi

# Перезапускаем OpenVPN, чтобы применить изменения в CRL
systemctl restart openvpn-server@server.service
if [ $? -ne 0 ]; then
    echo "Warning: Failed to restart OpenVPN. Manual restart may be required."
fi

# Очищаем правила iptables после перезапуска OpenVPN
if [ -n "$VIRTUAL_IP" ]; then
    # Удаляем правила, если они существуют
    iptables -D INPUT -s "$VIRTUAL_IP" -j DROP 2>/dev/null
    iptables -D OUTPUT -d "$VIRTUAL_IP" -j DROP 2>/dev/null
    echo "Cleaned up iptables rules for $VIRTUAL_IP."
    # Логируем снятие блокировки
    echo "$(date): Unblocked IP $VIRTUAL_IP for user $FULL_NAME" >> "$IPTABLES_LOG"
fi

# Удаляем клиентский файл и сертификаты
rm -f "$CLIENT_DIR/$ID.ovpn"
rm -f "$CLIENT_DIR/$FULL_NAME.crt"
rm -f "$CLIENT_DIR/$FULL_NAME.key"
rm -f "$EASYRSA_DIR/pki/reqs/$FULL_NAME.req"
rm -f "$EASYRSA_DIR/pki/issued/$FULL_NAME.crt"
rm -f "$EASYRSA_DIR/pki/private/$FULL_NAME.key"

echo "User $FULL_NAME deleted successfully. Access revoked and active connection terminated."
exit 0
