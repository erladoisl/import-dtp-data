# Модуль для создания запросов для получения файлов из сайта http://stat.gibdd.ru/
# в котором информация с карточек ДТП по всему татарстану


from typing import List, Dict, Union
import requests
import zipfile
from io import BytesIO
import os
import json

# ЗАДАЧА 42: нужно дополнить переменную REGIONS. Уточнить в чате, каким образом это нужно сделать
REGIONS = {'Атнинский район': 92213,
           "Буинский район": 92218, "Сабинский район": 92252}

# Адрес для получения ид файла
GETTING_FILE_ID_URL = "http://stat.gibdd.ru/map/getDTPCardDataXML"

# Адрес для загрузки файла архивом с ид, полученным по ссылке выше
DOWNLOAD_FILE_BY_ID_URL = 'http://stat.gibdd.ru/getPDFbyId?data='


def get_months(start_month: int, end_month: int, year: int) -> List[str]:
    '''
        Возвращает список из строк: "MONTHS:{startMonth}.{year}", ... MONTHS:{endMonth}.{year}"

        Добавить проверку на месяц: 
        1. не меньше 1, не больше 12
        2. startMonth < endMonth
        Если startMonth > endMonth, поменять значения местами

        >>> get_months(1, 4, 2021)
        ['MONTHS:1.2021', 'MONTHS:2.2021', 'MONTHS:3.2021', 'MONTHS:4.2021']
        >>> get_months(4, 12, 2021)
        ['MONTHS:4.2021', 'MONTHS:5.2021', 'MONTHS:6.2021', 'MONTHS:7.2021', 'MONTHS:8.2021', 'MONTHS:9.2021', 'MONTHS:10.2021', 'MONTHS:11.2021', 'MONTHS:12.2021']
    '''
    months = list()

    if start_month > end_month:
        start_month, end_month = end_month, start_month
    if start_month < 1:
        start_month = 1
    if end_month > 12:
        end_month = 12

    months = [f"MONTHS:{month}.{year}" for month in range(
        start_month, end_month + 1)]

    return months


def get_file_id_data(start_month: int, end_month: int, year: int, region: str) \
        -> str:
    '''
        Возвращает тело запроса для получения ид файла в виде словаря объекта

        Тело запроса сформировать в виде словаря:
        {"date": ["MONTHS:1.2021", "MONTHS:2.2021", "MONTHS:3.2021", "MONTHS:4.2021", "MONTHS:5.2021", "MONTHS:6.2021", "MONTHS:7.2021", "MONTHS:8.2021", "MONTHS:9.2021", "MONTHS:10.2021", "MONTHS:11.2021", "MONTHS:12.2021"],
         "ParReg":"92",
         "order": {"type": "1", "fieldName": "dat"},
         "reg": "42", "ind": "1", "st": "1", "en": "7"}
        Значение поля date берется из функции getMonths()
        Значение поля reg - значение по ключу region в глобальной константе-словаре REGIONS
        Далее конвертировать словарь в json объект и вернуть его

        >>> get_file_id_data(2, 4, 2021, 'Атнинский район')
        {'date': ['MONTHS:2.2021', 'MONTHS:3.2021', 'MONTHS:4.2021'], 'ParReg': '92', 'order': {'type': '1', 'fieldName': 'dat'}, 'reg': '92213', 'ind': '1', 'st': '1', 'en': '7'}
        >>> get_file_id_data(6, 4, 2021, 'Буинский район')
        {'date': ['MONTHS:4.2021', 'MONTHS:5.2021', 'MONTHS:6.2021'], 'ParReg': '92', 'order': {'type': '1', 'fieldName': 'dat'}, 'reg': '92218', 'ind': '1', 'st': '1', 'en': '7'}
    '''
    result_dict = '{"date":' + \
                  f'{get_months(start_month, end_month, year)}, ' + \
                  '"ParReg": "92", ' + \
                  '"order": {"type": "1", "fieldName": "dat"},' + \
                  f'"reg": {REGIONS[region]}, ' + \
                  '"ind": "1", "st": "1", "en": "7"}'

    return result_dict.replace('\'', '\"')


def get_files_id(start_month: int, end_month: int, year: int, region: str) -> str:
    '''
        Возвращает ид документа, который нужно скачать
        Сделать post запрос, используя библиотеку requests:
        по адресу GETTING_FILE_ID_URL
        в теле запроса data установить значение которое, вернула ф-я get_file_id_data
        Получить информацию в виде json-объекта
        Вернуть значение под ключом data в этом json-объекте

        >>> type(get_files_id(1, 2, 2021, 'Атнинский район'))
        <class 'int'>
    '''
    data = get_file_id_data(start_month, end_month, year, region)
    page = requests.post(GETTING_FILE_ID_URL, data=json.dumps({'data': data}),
                         headers={'Content-type': 'application/json'})
    file_id = page.json()

    return file_id["data"]


def download_dtp_data_xml_file(file_id: str, region: str, folder: str = 'result') -> None:
    '''
        Загрузка файлов по file_id

        Сделать get запрос по DOWNLOAD_FILE_BY_ID_URL, используя библиотеку requests:
        в качестве параметра запроса data установить file_id
        Получить контент ответа на запрос в виде байтового представления архива с файлом
        Создать папку с названием folder в корне текущего файла с кодом.
        С помощью библиотеки zipfile и метода BytesIO сохранить в папку с названием {folder}/{region}
        содержимое архива - файл с расширением xml
    '''
    page = requests.get(DOWNLOAD_FILE_BY_ID_URL + file_id)
    xml_file = zipfile.ZipFile(BytesIO(page.content))
    address = f'{folder}/{region}'
    xml_file.extractall(address)


def get_tatarstan_dtp_data(start_month: int, end_month: int, year: int, region: str = "") -> None:
    '''
        Получение файлов xml с данными о ДТП для всех районов Татарстана

        ВАЖНО: Перед реализацией этой ф-ии нужно выполнить "ЗАДАЧА 42"

        Для всех ключей в глобальной переменной REGIONS:
            1. получить id файла как результат выполнения ф-ии get_files_id() при 
               аргументах: startMonth, endMonth, year и текущий ключ как значение переменной region
            2. выполнить ф-ю download_dtp_data_xml_file с значениями аргументов:
                file_id = id файла, полученным в предыдущем пункте,
                region = текущий ключ     
        #### Не реализовано ->
        Если сторока региона пуста, то нужно пройтись по всем регионам 

    '''
    for region_name, region_id in REGIONS.items():
        file_id = get_files_id(start_month, end_month, year, region_name)
        download_dtp_data_xml_file(file_id, region_name)
    #first_directory_XML_files = './result'
    #directory_of_files = os.listdir(directory_XML_files)
    #print(files)

# https://pythoner.name/walk - библиотека для этой функции
def finder_to_xml_name(): # функция для помещения в лист всех названий файлов( для передачи в узел как входящий параметр)
    names = os.listdir(os.getcwd('./request'))
    for name in names:
        fullname = os.path.join(os.getcwd(), name)
        if os.path.isfile(fullname):
            os.rename('Список карточек ДТП.xml','{names}.xml')

if __name__ == "__main__":
     get_tatarstan_dtp_data(1, 2, 2021)
    #get_tatarstan_dtp_data(int(global_dict["startMonth"]), int(global_dict["endMonth"]), int(global_dict["year"]))