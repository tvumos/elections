# elections
Программа сбора результатов выборов по всем участковым избирательным комисиям города Москвы.
На сайте МОСКОВСКОЙ ГОРОДСКОЙ ИЗБИРАТЕЛЬНОЙ КОМИССИИ, к сожалению отсутствуют данные в формате
доступном для дальнейшей обработки. Программа разрабатывалась в рамках проекта по контролю за выборами, для
сверки официальных результатов из системы ГАС «Выборы» и результатов полученных по результату просмотра
видео с избирательных участков. Задача - контроль количества проголосовавших граждан на избирательном участке.
Использовались данные размещенные на сайте МОСКОВСКОЙ ГОРОДСКОЙ ИЗБИРАТЕЛЬНОЙ КОМИССИИ
с результатами выборов Мэра города Москвы 09.09.2018:
http://www.moscow_city.vybory.izbirkom.ru/region/region/moscow_city?action=show&root=1&tvd=27720002197406&vrn=27720002197402&region=77&global=&sub_region=77&prver=0&pronetvd=null&vibid=27720002197406&type=234

Первая версия данной программы была реализована с использованием библиотеки Selenium и C#.
Задача была решена, но код получился достаточно громоздкий.
После знакомства с библиотекой BeautifulSoup возникла идея реализовать задачу на Python.
Программа на выходе создает файлы CSV с выгруженными результатами голосования на выборах Мэра Москвы
по всем УИК г.Москвы для дальнейшей загрузки в любую базу данных.
В связи с тем, что на сайте МОСКОВСКОЙ ГОРОДСКОЙ ИЗБИРАТЕЛЬНОЙ КОМИССИИ практически не используются css классы
пришлось использовать библиотеку lxml для построения xpath запросов.

Для работы программы необходимо установить:
1) BeautifulSoup:
        pip install beautifulsoup4
2) requests
3) lxml

Общее время обработки составило: 904 секунд




