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

# Путь к easy-rsa и другим директориям
EASYRSA_DIR="/etc/openvpn/easy-rsa"
CLIENT_DIR="/etc/openvpn/server/clients"
CLIENT_CONF="$CLIENT_DIR/$ID.ovpn"

# Проверка, что easy-rsa существует
if [ ! -d "$EASYRSA_DIR" ]; then
    echo "Error: Directory $EASYRSA_DIR not found. Please install easy-rsa."
    exit 1
fi

# Создание директории для клиентских файлов, если не существует
mkdir -p "$CLIENT_DIR"

# Переходим в easy-rsa
cd "$EASYRSA_DIR"

# Удаляем старые файлы EasyRSA, если они существуют
rm -f "pki/reqs/$FULL_NAME.req"
rm -f "pki/issued/$FULL_NAME.crt"
rm -f "pki/private/$FULL_NAME.key"

# Генерация сертификата и ключа для нового пользователя
./easyrsa build-client-full "$FULL_NAME" nopass
if [ $? -ne 0 ]; then
    echo "Error: Failed to generate certificates for $FULL_NAME."
    exit 1
fi

# Копируем необходимые файлы
cp "pki/ca.crt" "$CLIENT_DIR/"
cp "pki/issued/$FULL_NAME.crt" "$CLIENT_DIR/"
cp "pki/private/$FULL_NAME.key" "$CLIENT_DIR/"

# Создаём клиентский файл .ovpn
cat > "$CLIENT_CONF" << EOF
client
dev tun
proto udp
remote 178.208.64.133 1194
nobind
remote-cert-tls server
cipher CHACHA20-POLY1305
verb 3

<ca>
$(cat "$CLIENT_DIR/ca.crt")
</ca>

<cert>
$(cat "$CLIENT_DIR/$FULL_NAME.crt")
</cert>

<key>
$(cat "$CLIENT_DIR/$FULL_NAME.key")
</key>

dhcp-option DNS 8.8.8.8
dhcp-option DNS 8.8.4.4
tun-mtu 1400
mssfix 1360
EOF

# Проверка, что файл .ovpn содержит сертификаты
if ! grep -q "BEGIN CERTIFICATE" "$CLIENT_CONF"; then
    echo "Error: Generated .ovpn file is invalid (certificates missing)."
    exit 1
fi

echo "User $FULL_NAME added successfully. Client file created at $CLIENT_CONF."
exit 0
