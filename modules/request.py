# Модуль для создания запросов для получения файлов из сайта http://stat.gibdd.ru/
# в котором информация с карточек ДТП по всему татарстану


from typing import List
import requests
import zipfile
from io import BytesIO
import os
import json

# ЗАДАЧА 42: нужно дополнить переменную REGIONS. Уточнить в чате, каким образом это нужно сделать
REGIONS = {'Атнинский район': 92213, "Буинский район": 92218, "Сабинский район": 92252}

# Адрес для получения ид файла
GETTING_FILE_ID_URL = "http://stat.gibdd.ru/map/getDTPCardDataXML"

# Адрес для загрузки файла архивом с ид, полученным по ссылке выше
DOWNLOAD_FILE_BY_ID_URL = 'http://stat.gibdd.ru/getPDFbyId?data='


def get_months(startMonth: int, endMonth: int, year: int) -> List[str]:
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
    result_list = list()
    if startMonth > endMonth:
        startMonth, endMonth = endMonth, startMonth
    if startMonth < 1:
        startMonth = 1
    if endMonth > 12:
        endMonth = 12

    for month in range(startMonth, endMonth + 1):
        element = f"MONTHS:{month}.{year}"
        result_list.append(element)
    return result_list



def get_file_id_data(startMonth: int, endMonth: int, year: int, region: str) -> str:
    '''
        Возвращает тело запроса для получения ид файла в виде json объекта

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
    pass


def get_files_id(startMonth: int, endMonth: int, year: int, region: str) -> int:
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
    pass
    # # доделать возврат данных из функции get_file_id_data для подстановки в "params_for_post = {"data"...
    # params_for_post = {"data" = ""}
    # download_file_id = requests.post(GETTING_FILE_ID_URL, json=params_for_post)
    # # download_file_id.json() # преобразование в json-объект


def download_dtp_data_xml_file(file_id: int, region: str, folder: str = 'result') -> None:
    '''
        Загрузка файлов по file_id

        Сделать get запрос по DOWNLOAD_FILE_BY_ID_URL, используя библиотеку requests:
        в качестве параметра запроса data установить file_id
        Получить контент ответа на запрос в виде байтового представления архива с файлом
        Создать папку с названием folder в корне текущего файла с кодом.
        С помощью библиотеки zipfile и метода BytesIO сохранить в папку с названием {folder}/{region}
        содержимое архива - файл с расширением xml
    '''
    pass
    # # get запрос
    # params_for_get = {"key": "file_id"}
    # file_ID_get = requests.get(DOWNLOAD_FILE_BY_ID_URL, params=params_for_get)
    # print(file_ID_get.url)
    # # представление ответа в байтовом виде в переменной "file_ID_open"
    # # file_ID_open = file_ID_get.open(BytesIO(requests.content))
    # os.mkdir("folder")
    # # Извлечение  файла
    # archive = 'file.zip'


# with zipfile.ZipFile(archive, 'r') as zip_file:
#     zip_file.extractall("folder")


def get_tatarstan_dtp_data(startMonth: int, endMonth: int, year: int) -> None:
    '''
        Получение файлов xml с данными о ДТП для всех районов Татарстана

        ВАЖНО: Перед реализацией этой ф-ии нужно выполнить "ЗАДАЧА 42"

        Для всех ключей в глобальной переменной REGIONS:
            1. получить id файла как результат выполнения ф-ии get_files_id() при
               аргументах: startMonth, endMonth, year и текущий ключ как значение переменной region
            2. выполнить ф-ю download_dtp_data_xml_file с значениями аргументов:
                file_id = id файла, полученным в предыдущем пункте,
                region = текущий ключ
    '''
    pass