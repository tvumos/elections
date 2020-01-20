import telebot
import requests
from telebot import apihelper, types
from bs4 import BeautifulSoup
import time
import csv

# ============== SETTING =====================================
MAX_DELAY = 2000        # Ограничение максимальной задержки для искомого proxy мс
MAX_RETURN = 20          # Максимальное количество повторений запуска бота, при превышении - программа завершается
region_in_page = 10     # Количество кнопок с регионами на странице
url = 'http://www.moscow_city.vybory.izbirkom.ru/region/region/moscow_city?action=show&root=1&tvd=27720002197406&vrn=27720002197402&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720002197406&type=234'
# =============================================================

# ============== CONST ========================================
TKN = '<TOKEN>'       # Токен бота
BOT_ID = 807168173                                          # Идентификатор бота
BOT_USER_NAME = 'VotingResultsBot'                          # Администратор бота
RUSSIA = 'Russian Federation'                               # Страна, пропускаемая при поиске PROXY
PROXIES_TEMPLATE = {
    'http': 'http://51.158.98.121:8811',
    'https': 'http://51.158.98.121:8811'
}
# =============================================================

# Start program
# Запрос страницы выборов
response = requests.get(url)
# Создаем soup для разбора html
soup = BeautifulSoup(response.text, 'html.parser')

bot = telebot.TeleBot(TKN)

current_max_region = 0
current_page = 0
dict_regions = {}
regions_tag = soup.find_all('option')
for region in regions_tag:      # ОТЛАДКА Удалить ограничение в 2 региона
    region_name = region.text
    region_ind = region_name.split()[0]
    region_name = region_name.replace(str(region_ind), '', 1).strip()
    url_region = region.get('value')
    if len(region_name) > 0:
        dict_regions[str(region_ind) + ' ' + region_name] = url_region
# Создаем список из словарей нужного размера, для каждой страницы = region_in_page
dict_page = {}
list_regions =[]
for ind, region in enumerate(dict_regions.items()):
    if ind % region_in_page == 0 and not ind == 0:   # Последний элемент на странице
        if len(dict_page) > 0:
            list_regions.append(dict_page)
            dict_page = {}
            dict_page[region[0]] = region[1]
    else:
        dict_page[region[0]] = region[1]

list_regions.append(dict_page)
# pprint.pprint(list_regions)
# print(len(list_regions))



def pages_keyboard(regions_list, number_page):
    """Формируем Inline-кнопки для перехода по страницам.
    """
    global current_page

    keyboard = types.InlineKeyboardMarkup()
    # keyboard.row_width = 3
    for temp in regions_list[number_page].items():
        keyboard.row(types.InlineKeyboardButton(text=temp[0], callback_data=temp[0], url=temp[1]))

    if number_page == 0:
        keyboard.add(types.InlineKeyboardButton(text='След.', callback_data='next'))
    elif number_page == len(regions_list) - 1:
        keyboard.add(types.InlineKeyboardButton(text='Пред.', callback_data='back'))
    else:
        keyboard.add(types.InlineKeyboardButton(text='Пред.', callback_data='back'),
                     types.InlineKeyboardButton(text='След.', callback_data='next'))

    current_page = number_page
    return keyboard     # возвращаем объект клавиатуры


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def process_callback_back(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Выберите район',
                     reply_markup=pages_keyboard(list_regions, current_page - 1))


@bot.callback_query_handler(func=lambda c: c.data == 'next')
def process_callback_next(callback_query: types.CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Выберите район',
                     reply_markup=pages_keyboard(list_regions, current_page + 1))


@bot.message_handler(commands=['result'])
def send_files(message):
    bot.reply_to(message, "Отправляем файлы с результатами выборов Мэра Москвы 09.09.2018")
    with open('Description.csv', 'r', encoding='utf-8') as f:
        bot.send_document(message.chat.id, f)
    with open('Moscow_09_09_2018.csv', 'r', encoding='utf-8') as f:
        bot.send_document(message.chat.id, f)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Этот бот отображает результаты выборов мэра Москвы")


@bot.message_handler(commands=['start'])
def send_start(message):
    global current_page
    current_page = 0
    bot.send_message(message.chat.id, 'Укажите интересующий район',
                     reply_markup=pages_keyboard(list_regions, current_page))


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
                except Exception as err:
                    # print(f'ОШИБКА create_connect: {err}')
                    time.sleep(1)
                    continue
    return numb


count_return = 0
i = 0
while True:
    try:
        if count_return >= MAX_RETURN:
            print(f'Выполнено подключение к {count_return} proxy, соединения разорваны серверами. '
                  f'Замените файл со списком proxy. Программа завершена')
            break
        i = create_connect(i)
        # bot.polling(none_stop=True, timeout=0.001)  # ОТЛАДКА
        bot.polling(none_stop=False, timeout=10)
    except Exception as err:
        count_return += 1
        print(f'Proxy сервер разорвал соединение. Попытка № {count_return}, ОШИБКА: {err.args}')
        continue
