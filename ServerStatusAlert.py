from mcstatus import JavaServer
from datetime import datetime
import requests
import time

server_address = 'YOUR_SERVER_ADDRESS'
online_check_interval = 60 * 5
offline_check_interval = 60 * 1
bot_token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
message_offline = 'я упал'
message_online = 'я встал'


def get_server_status(ip):
    try:
        server = JavaServer.lookup(ip)
        status = server.status()
        return {
            'online': True,
            'players': status.players.online,
            'max_players': status.players.max
        }
    except:
        return {
            'online': False
        }


def send_telegram_message(token, chat, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    params = {'chat_id': chat, 'text': message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f'[{datetime.today().strftime("%d.%m.%Y %H:%M:%S")}] Сообщение "{message}" отправлено в Telegram')
    else:
        print(f'[{datetime.today().strftime("%d.%m.%Y %H:%M:%S")}] Cообщение "{message}" не удалось отправить '
              f'в Telegram ({response.status_code} {response.json()["description"]})')


was_online = True
while True:
    result = get_server_status(server_address)
    if result['online']:
        print(f'[{datetime.today().strftime("%d.%m.%Y %H:%M:%S")}] Сервер {server_address} работает: '
              f'{result["players"]}/{result["max_players"]} игроков')
        if not was_online:
            send_telegram_message(bot_token, chat_id, message_online)
            was_online = True
    else:
        print(f'[{datetime.today().strftime("%d.%m.%Y %H:%M:%S")}] Сервер {server_address} не работает')
        if was_online:
            send_telegram_message(bot_token, chat_id, message_offline)
            was_online = False
    time.sleep(online_check_interval if result['online'] else offline_check_interval)
