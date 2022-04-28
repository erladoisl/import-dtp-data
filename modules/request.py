# Модуль для создания запросов для получения файлов

from typing import List
import requests
import zipfile
from io import BytesIO

TAG_NAMES = ["date", "DTPV", "district", "street", "house", "time", "kartId", "COORD_L", "COORD_W", "k_ul", "km", "m",
             "KTS", "KUCH", "POG", "RAN", "sdor", "spog", "osv", "factor", "ndu", "OBJ_DTP", "s_pch"]
# нужные нам теги, перевод с тэга на русский, учитывая, что они несколько раз могут встречаться
TRANSLATION = {'date': 'дата', 'DTPV': 'вид дтп', 'district': 'место', 'street': 'улица', 'house': 'дом',
               'time': 'время', 'kartId': 'номер', 'COORD_L': 'долгота', 'COORD_W': 'широта', 'k_ul': 'дорога',
               'km': 'километр', 'm': 'метр', 'KTS': 'количество транспортных средств', 'KUCH': 'количество участников',
               'POG': 'погибло', 'RAN': 'ранены', 'sdor': 'состояние дороги', 'spog': 'состояние погоды',
               'osv': 'освещение', 'factor': 'факторы',
               'ndu1': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети1',
               'ndu2': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети2',
               'ndu3': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети3',
               'OBJ_DTP1': 'Объекты УДС вблизи места ДТП1', 'OBJ_DTP2': 'Объекты УДС вблизи места ДТП2',
               'OBJ_DTP3': 'Объекты УДС вблизи места ДТП3', 'OBJ_DTP4': 'Объекты УДС вблизи места ДТП4',
               'OBJ_DTP5': 'Объекты УДС вблизи места ДТП5', 'OBJ_DTP6': 'Объекты УДС вблизи места ДТП6',
               's_pch': 'состояние проезжей части'}

MULTIPLE_VALUES = ['OBJ_DTP', 'ndu']  # те, кто несколько раз встречаются

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
        ["MONTHS:1.2021", "MONTHS:2.2021", "MONTHS:3.2021", "MONTHS:4.2021"]
        >>> get_months(4, 12, 2021)
        ["MONTHS:1.2021", "MONTHS:2.2021", "MONTHS:3.2021", "MONTHS:4.2021"]
    '''
    pass


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