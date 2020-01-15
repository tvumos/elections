import requests
import datetime
from bs4 import BeautifulSoup
from lxml import html
# import pprint


DELIMITER = '|'
url = 'http://www.moscow_city.vybory.izbirkom.ru/region/region/moscow_city?action=show&root=1&tvd=27720002197406&vrn=27720002197402&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720002197406&type=234'
FILE_NAME_DESCRIPTION = 'Description.csv'
FILE_NAME_RESULT = 'Moscow_09_09_2018.csv'


def save_header_to_file(dict_header):
    with open(FILE_NAME_DESCRIPTION, 'w', encoding='utf-8') as f:
        f_numb = 0
        f.write(f'field_name{DELIMITER}numb_row{DELIMITER}description' + '\n')
        for numb, desk in dict_header.items():
            f_numb += 1
            f.write(f'F{f_numb}{DELIMITER}{numb}{DELIMITER}{desk}' + '\n')


def save_result_to_file(city_id, city_name, region_id, region_name, uik_id, uik_name, result_str):
    with open(FILE_NAME_RESULT, 'a', encoding='utf-8') as f:
        f.write(f'{city_id}{DELIMITER}{city_name}{DELIMITER}{region_id}{DELIMITER}'
                f'{region_name}{DELIMITER}{uik_id}{DELIMITER}{uik_name}{DELIMITER}{result_str}' + '\n')


def save_header_to_result_file():
    with open(FILE_NAME_RESULT, 'w', encoding='utf-8') as f:
        f.write(f'city_id{DELIMITER}city_name{DELIMITER}region_id{DELIMITER}region_name{DELIMITER}'
                f'uik_id{DELIMITER}uik_name{DELIMITER}F1{DELIMITER}F2{DELIMITER}F3{DELIMITER}F4{DELIMITER}'
                f'F5{DELIMITER}F6{DELIMITER}F7{DELIMITER}F8{DELIMITER}F9{DELIMITER}F10{DELIMITER}F11{DELIMITER}'
                f'F12{DELIMITER}F13{DELIMITER}F14{DELIMITER}F15{DELIMITER}F16{DELIMITER}' + '\n')


def parsing_page_header(lxml_page):
    result = {}
    for i in range(1, 18):
        numb = lxml_page.xpath(f'//html/body/table[3]/tr[4]/td/table[5]/tr[{i}]/td[1]/text()')
        desk = lxml_page.xpath(f'//html/body/table[3]/tr[4]/td/table[5]/tr[{i}]/td[2]/text()')
        if len(numb) == 1:
            result[numb[0]] = desk[0]
    return result


def parsing_page_value(lxml_page):
    result = ""
    for i in range(1, 18):
        val = lxml_page.xpath(f'//html/body/table[3]/tr[4]/td/table[5]/tr[{i}]/td[3]/b/text()')
        if len(val) == 1:
            result += str(val[0]) + DELIMITER
    return result


start = datetime.datetime.now()
print('========= Начинаем обработку результатов выборов Мэра Москвы 09.09.2018 ==============================')
# Запрос страницы выборов
response = requests.get(url)
# Создаем soup для разбора html
soup = BeautifulSoup(response.text, 'html.parser')
#pprint.pprint(soup)
# Получаем страницу для выполнения запросов XPath
page_body = html.fromstring(response.text, parser=html.HTMLParser(encoding='utf-8'))
# Получаем расшифровку строк
dict_header = parsing_page_header(page_body)
# Сохраняем описание полей в файл c главной страницы с результатами
save_header_to_file(dict_header)

id_city = 1
name_city = 'Москва'
id_region = ''
name_region = ''
id_uik = ''
name_uik = ''
save_header_to_result_file()
str_result = parsing_page_value(page_body)
save_result_to_file(id_city, name_city, id_region, name_region, id_uik, name_uik, str_result)

# Получаем список районов на главной странице
regions_tag = soup.find_all('option')
for region in regions_tag:      # ОТЛАДКА Удалить ограничение в 2 региона
    region_name = region.text
    region_ind = region_name.split()[0]
    region_name = region_name.replace(str(region_ind), '', 1).strip()
    url_region = region.get('value')
    if len(region_name) > 0:
        # print(f'Region index={region_ind}; name={region_name}')
        # print(url_region)

        # Получаем список УИКов по каждому региону
        response_region = requests.get(url_region)
        region_soup = BeautifulSoup(response_region.text, 'html.parser')
        page_body = html.fromstring(response_region.text, parser=html.HTMLParser(encoding='utf-8'))
        str_result = parsing_page_value(page_body)
        save_result_to_file(id_city, name_city, region_ind, region_name, id_uik, name_uik, str_result)
        uiks_tag = region_soup.find_all('option')
        for uik_tag in uiks_tag:
            uik_name = uik_tag.text
            uik_ind = uik_name.split()[0]
            uik_name = uik_name.replace(str(uik_ind), '', 1).strip()
            url_uik = uik_tag.get('value')
            if len(uik_name) > 0:
                # print(f'UIK index={uik_ind}; name={uik_name}')
                # print(url_uik)
                response_uik = requests.get(url_uik)
                page_body = html.fromstring(response_uik.text, parser=html.HTMLParser(encoding='utf-8'))
                str_result = parsing_page_value(page_body)
                save_result_to_file(id_city, name_city, region_ind, region_name, uik_ind, uik_name, str_result)

delta = datetime.datetime.now() - start
print(f'========= Обработка результатов выборов завершена. Обработка выполнена за {delta.seconds} секунд ==================')








