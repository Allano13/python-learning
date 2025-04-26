# config.py
# Конфигурация бота: токены, пути и состояния

TOKEN = "7923851324:AAHtpz9b5WjTZA9-swGFKtkzKGq3qZLKFEU"
ADMIN_ID = "5208462139"
DB_PATH = "/root/admin_bot/admin_users.db"
INSTRUCTION_PATH = "/root/admin_bot/resources/instruction_iphone.pdf"
SEND_KEY_SCRIPT = "/root/admin_bot/scripts/send_key.sh"
GENERATE_KEY_SCRIPT = "/root/admin_bot/scripts/generate_key.sh"
DELETE_KEY_SCRIPT = "/root/admin_bot/scripts/delete_key.sh"
ID_STATE, NAME_STATE, DELETE_STATE, ISSUE_KEY_STATE = range(4)
