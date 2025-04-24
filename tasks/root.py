import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"  # Укажи свой путь к Graphviz

from graphviz import Digraph

# Создаём граф с вертикальной ориентацией (сверху вниз)
dot = Digraph(comment='File Structure Schema', format='png')
dot.attr('graph', rankdir='TB')  # Устанавливаем направление сверху вниз
dot.attr('node', shape='box', style='filled', fillcolor='lightblue')
dot.attr('edge', color='blue')

# Функция для добавления узлов и связей
def add_node(parent, name, label=None, is_file=True):
    node_id = f"{parent}_{name}" if parent else name
    dot.node(node_id, label if label else name, fillcolor='lightyellow' if is_file else 'lightblue')
    if parent:
        dot.edge(parent, node_id)

# Корневые узлы
add_node(None, '/root', is_file=False)
add_node(None, '/etc', is_file=False)

# /root
add_node('/root', 'list_users.sh', 'list_users.sh\n# Отображает список\n# пользователей и отправляет\n# в Telegram')
add_node('/root', 'delete_user.sh', 'delete_user.sh\n# Удаляет пользователя\n# OpenVPN (отзывает сертификат,\n# обновляет CRL)')
add_node('/root', 'send_user_key.sh', 'send_user_key.sh\n# Отправляет .ovpn файл\n# пользователя в Telegram')
add_node('/root', 'add_user.sh', 'add_user.sh\n# Добавляет нового\n# пользователя (генерирует .ovpn,\n# отправляет в Telegram)')
add_node('/root', 'disable_firewall.sh', 'disable_firewall.sh\n# Отключает брандмауэр\n# (ufw и iptables)')
add_node('/root', 'script_summary.txt', 'script_summary.txt\n# Документация:\n# Описание скриптов и настроек')
add_node('/root', 'instructions.txt', 'instructions.txt\n# Инструкция:\n# Руководство по скриптам OpenVPN')

# /root/client-configs
add_node('/root', 'client-configs', 'client-configs/', is_file=False)
add_node('/root_client-configs', 'make_config.sh', 'make_config.sh\n# Генерирует .ovpn файл\n# для клиента OpenVPN')

# /root/admin_bot
add_node('/root', 'admin_bot', 'admin_bot/', is_file=False)
add_node('/root_admin_bot', 'admin_bot.py', 'admin_bot.py\n# Код Telegram-бота')
add_node('/root_admin_bot', 'admin_users.db', 'admin_users.db\n# База данных\n# пользователей')
add_node('/root_admin_bot', 'resources', 'resources/', is_file=False)
add_node('/root_admin_bot_resources', 'instruction_iphone.pdf', 'instruction_iphone.pdf\n# Инструкция для iPhone')

# /etc/openvpn
add_node('/etc', 'openvpn', 'openvpn/', is_file=False)

# /etc/openvpn/easy-rsa
add_node('/etc_openvpn', 'easy-rsa', 'easy-rsa/', is_file=False)
add_node('/etc_openvpn_easy-rsa', 'update_server_conf.sh', 'update_server_conf.sh\n# Обновляет конфигурацию\n# сервера (шифрование,\n# MTU/MSS)')
add_node('/etc_openvpn_easy-rsa', 'update_client_conf.sh', 'update_client_conf.sh\n# Обновляет шаблон\n# клиента (newclient.ovpn)')
add_node('/etc_openvpn_easy-rsa', 'pki', 'pki/', is_file=False)
add_node('/etc_openvpn_easy-rsa_pki', 'index.txt', 'index.txt\n# Список сертификатов:\n# Действующие и отозванные')

# /etc/openvpn/server
add_node('/etc_openvpn', 'server', 'server/', is_file=False)
add_node('/etc_openvpn_server', 'clients', 'clients/\n# Папка с ключами\n# пользователей', is_file=False)
add_node('/etc_openvpn_server_clients', 'ca.crt', 'ca.crt\n# Сертификат CA\n# для клиентов')
add_node('/etc_openvpn_server', 'ca.crt', 'ca.crt\n# Сертификат CA\n# (для сервера)')
add_node('/etc_openvpn_server', 'server.conf', 'server.conf\n# Конфигурация\n# сервера')
add_node('/etc_openvpn_server', 'server.crt', 'server.crt\n# Сертификат\n# сервера')
add_node('/etc_openvpn_server', 'server.key', 'server.key\n# Ключ сервера')
add_node('/etc_openvpn_server', 'dh.pem', 'dh.pem\n# Параметры\n# Диффи-Хеллмана')
add_node('/etc_openvpn_server', 'ta.key', 'ta.key\n# Ключ TLS\n# (для защиты)')
add_node('/etc_openvpn_server', 'newclient.ovpn', 'newclient.ovpn\n# Шаблон для\n# новых клиентов')
add_node('/etc_openvpn_server', 'crl.pem', 'crl.pem\n# Список отозванных\n# сертификатов')

# Сохраняем схему в файл schema.png
dot.render('schema', view=False)
print("Schema generated as schema.png in the project directory.")