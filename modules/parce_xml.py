# Модель в котором по всему татарстану загружается информация с карточек ДТП из сайта http://stat.gibdd.ru/


from typing import Dict, List
import xml.etree.ElementTree as ET
from request import get_tatarstan_dtp_data
from pandas import DataFrame
from os import listdir

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

MULTIPLE_VALUES = ['OBJ_DTP', 'ndu']  # те, что несколько раз встречаются


# ЗАДАЧА 42: упростить ф-ю read_xml, разбить на подфункции
# определить типы входных и исходящих аргументов
def read_xml(xml: ET.Element, data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    multiple_values_dict = dict(zip(MULTIPLE_VALUES, [0] * len(MULTIPLE_VALUES)))
    for child in xml:
        if len(child):
            if child.tag == "tab":
                for key, value in data.items():
                    data[key].append("")
            read_xml(child, data)
        else:
            if child.tag in TAG_NAMES:
                add_to_dtp_data(data, multiple_values_dict, child.tag, child.text)
    return data


def add_to_dtp_data(data: Dict[str, List[str]], mul_val_dict: Dict[str, int], tag: str, text: str) -> None:
    if tag in MULTIPLE_VALUES:
        mul_val_dict[tag] += 1
        count = mul_val_dict[tag]
        data[TRANSLATION[f'{tag}{count}']][-1] = text
    else:
        data[TRANSLATION[tag]][-1] = text


def get_tree(district: str) -> ET.Element:
    """
        Возвращает дерево элементов в файле xml
        
        Получить содержимое файла "Список карточек ДТП.xml", находящийся в папке district:
        Использовать библиотеку ET, получить дерево элементов в файле xml
        Вернуть дерево элементов

        :param district: название эксель файла
        :param data: данные с карточек ДТП
        :return:
        
        >>> tree = get_tree('test\Атнинский район')
        >>> f'{tree[4].text} - {tree[7].text}' 
        'ДТП - всего - Республика Татарстан (Татарстан), Атнинский район'
        >>> type(tree) == ET.Element
        True
    """
    address = f'{district}\Список карточек ДТП.xml'
    tree = ET.parse(address)
    root = tree.getroot()
    return root


def get_init_dict() -> Dict[str, List]:
    '''
        Создает словарь с ключами из TRANSLATION
        и значениями - пустой список
        Возвращает этот словарь
        
        >>> get_init_dict()
        {'дата': [], 'вид дтп': [], 'место': [], 'улица': [], 'дом': [], 'время': [], 'номер': [], 'долгота': [], 'широта': [], 'дорога': [], 'километр': [], 'метр': [], 'количество транспортных средств': [], 'количество участников': [], 'погибло': [], 'ранены': [], 'состояние дороги': [], 'состояние погоды': [], 'освещение': [], 'факторы': [], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети1': [], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети2': [], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети3': [], 'Объекты УДС вблизи места ДТП1': [], 'Объекты УДС вблизи места ДТП2': [], 'Объекты УДС вблизи места ДТП3': [], 'Объекты УДС вблизи места ДТП4': [], 'Объекты УДС вблизи места ДТП5': [], 'Объекты УДС вблизи места ДТП6': [], 'состояние проезжей части': []}
    '''
    return dict(zip(TRANSLATION.values(), [[] for i in range(len(TRANSLATION))]))


def parse_xml(district: str, data: Dict[str, List[str]]) -> Dict[str, List[str]]:
    '''
        Добавляет в data информацию о ДТП по району district
        
        Выполнить get_tree() и получить дерево элементов в файле xml для district
        Выполнить read_xml() с аргументами: дерево элементов и data
        
        >>> test_data = get_init_dict()
        >>> parse_xml('test\Атнинский район', test_data)
        {'дата': ['16.12.2021'], 'вид дтп': ['Наезд на пешехода'], 'место': ['Атнинский р-н'], 'улица': [None], 'дом': [None], 'время': ['19:05'], 'номер': ['221934675'], 'долгота': ['49.306898'], 'широта': ['56.231162'], 'дорога': ['Вне НП'], 'километр': ['42'], 'метр': ['400'], 'количество транспортных средств': ['1'], 'количество участников': ['2'], 'погибло': ['0'], 'ранены': ['1'], 'состояние дороги': ['Перегон (нет объектов на месте ДТП)'], 'состояние погоды': ['Пасмурно'], 'освещение': ['В темное время суток, освещение отсутствует'], 'факторы': ['Сведения отсутствуют'], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети1': ['Не установлены'], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети2': [''], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети3': [''], 'Объекты УДС вблизи места ДТП1': ['Отсутствие в непосредственной близости объектов УДС и объектов притяжения'], 'Объекты УДС вблизи места ДТП2': [''], 'Объекты УДС вблизи места ДТП3': [''], 'Объекты УДС вблизи места ДТП4': [''], 'Объекты УДС вблизи места ДТП5': [''], 'Объекты УДС вблизи места ДТП6': [''], 'состояние проезжей части': ['Гололедица']}
    '''

    tree = get_tree(district)
    return read_xml(tree, data)


def save_to_excel(data: Dict[str, List[str]], folder: str = 'result') -> None:
    """
    сохраняет в эксель

    :folder: папка, куда сохранить документ
    :param data: данные с карточек ДТП
    :return:
    """
    DataFrame(data).to_excel(f"{folder}.xlsx", index=False)


def parse_tatarstan_DTP(folder: str = 'result') -> Dict[str, List[str]]:
    '''
        Парсит все файлы с информацией о ДТП в районах Татарстана, 
        сохраняет все в файл
        
        Получить пустой словарь с данными, выполнив ф-ю get_init_dict
        Пройтись по всем папкам из папки folder,
        выполняя ф-ию parse_xml с аргументами:
                district = folder + \название папки, data = словарь с данными
        Вернуть переменную со словарем с данными
        
        >>> parse_tatarstan_DTP('test')
        {'дата': ['16.12.2021', '12.12.2021'], 'вид дтп': ['Наезд на пешехода', 'Съезд с дороги'], 'место': ['Атнинский р-н', 'Буинский р-н'], 'улица': [None, None], 'дом': [None, None], 'время': ['19:05', '13:20'], 'номер': ['221934675', '221920778'], 'долгота': ['49.306898', '48.263218'], 'широта': ['56.231162', '54.937547'], 'дорога': ['Вне НП', 'Вне НП'], 'километр': ['42', '33'], 'метр': ['400', '273'], 'количество транспортных средств': ['1', '1'], 'количество участников': ['2', '3'], 'погибло': ['0', '0'], 'ранены': ['1', '2'], 'состояние дороги': ['Перегон (нет объектов на месте ДТП)', 'Перегон (нет объектов на месте ДТП)'], 'состояние погоды': ['Пасмурно', 'Ясно'], 'освещение': ['В темное время суток, освещение отсутствует', 'Светлое время суток'], 'факторы': ['Сведения отсутствуют', 'Сведения отсутствуют'], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети1': ['Не установлены', 'Не установлены'], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети2': ['', ''], 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети3': ['', ''], 'Объекты УДС вблизи места ДТП1': ['Отсутствие в непосредственной близости объектов УДС и объектов притяжения', 'Отсутствие в непосредственной близости объектов УДС и объектов притяжения'], 'Объекты УДС вблизи места ДТП2': ['', ''], 'Объекты УДС вблизи места ДТП3': ['', ''], 'Объекты УДС вблизи места ДТП4': ['', ''], 'Объекты УДС вблизи места ДТП5': ['', ''], 'Объекты УДС вблизи места ДТП6': ['', ''], 'состояние проезжей части': ['Гололедица', 'Мокрое']}
    '''
    data = get_init_dict()
    for elem in listdir(f"{folder}"):
        parse_xml(f"{folder}\{elem}", data)
    return data


if __name__ == '__main__':
    start_month = 1
    end_month = 2
    year = 2021

    # сохраним файлы с xml в папку result
    get_tatarstan_dtp_data(start_month, end_month, year)

    parsed_data = parse_tatarstan_DTP()
    save_to_excel(parsed_data)
