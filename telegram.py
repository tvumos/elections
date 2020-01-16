import telebot
from telebot import apihelper
import time
import csv

# ============== SETTING =====================================
MAX_DELAY = 1000    # Ограничение максимальной задержки для искомого proxy мс
MAX_RETURN = 3      # Максимальное количество повторений запуска бота, при превышении - программа завершается
# =============================================================

# ============== CONST ========================================
TKN = 'KEY_BOT'       # Токен бота
BOT_ID = 807168173                                          # Идентификатор бота
BOT_USER_NAME = 'VotingResultsBot'                          # Администратор бота
RUSSIA = 'Russian Federation'                               # Страна, пропускаемая при поиске PROXY
PROXIES_TEMPLATE = {
    'http': 'http://51.158.98.121:8811',
    'https': 'http://51.158.98.121:8811'
}
# =============================================================

# Start program
bot = telebot.TeleBot(TKN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    bot.process_new_channel_posts("Привет")


def create_connect(start_numb=0):
    is_first = True
    numb = 0
    with open('px_export.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            if is_first:
                is_first = False
                continue
            numb += 1
            if numb <= start_numb:
                continue
            row_arr = row[0].split(';')
            if row_arr[7] not in ('', RUSSIA) and int(row_arr[4]) < MAX_DELAY:
                proxies = PROXIES_TEMPLATE
                proxies['http'] = f'http://{row_arr[1]}:{row_arr[2]}'
                proxies['https'] = f'http://{row_arr[1]}:{row_arr[2]}'
                try:
                    print('Проверка работы proxy: ', f'http://{row_arr[1]}:{row_arr[2]}')
                    apihelper.proxy = proxies
                    # Проверка соединения и получение информации по боту
                    bot_help = apihelper.get_me(TKN)
                    if bot_help['id'] == BOT_ID and bot_help['username'] == BOT_USER_NAME:
                        print("Рабочий сервер найден", 'Строка №', numb)
                        break
                    else:
                        continue
                except:
                    time.sleep(0.1)
                    continue
    return numb


count_return = 0
i = 0
while True:
    try:
        if count_return >= MAX_RETURN:
            print(f'Выполнено подключение к {count_return} proxy, соединения разорваны серверами. Программа завершена')
            break
        i = create_connect(i)
        # bot.polling(none_stop=True, timeout=0.001)  # ОТЛАДКА
        bot.polling(none_stop=False, timeout=10)
    except:
        count_return += 1
        print(f'Proxy сервер разорвал соединение. Попытка № {count_return}')
        continue
