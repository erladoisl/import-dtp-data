# -*- coding: cp1251 -*-
import xml.etree.ElementTree as ET
from pandas import ExcelWriter, DataFrame
import requests, zipfile
import json
from typing import Dict, List
from io import BytesIO
#I have changed something
print("Whasap brodi")

class Date:
    def __init__(self, date: str):
        """
        :param date: ����
        """
        self.month, self.year = date.split(".")
        self.month = int(self.month)
        self.year = int(self.year)

        if self.month > 12 or self.month < 1:
            raise Exception

    def __sub__(self, other) -> int:
        """
        �� ����� �� ���� ����� ������ �������� � �������
        :param other: ������ ������ Date
        :return: ������� � �������
        """
        return (self.month - other.month + 1) + 12 * (self.year - other.year)

    def __add__(self, offset: int) -> str:
        """
        �� ����� �� �������� � ��������� ���� ������ ������ �����.���
        :param other: ��������
        :return: �����.���
        """
        # (���. ����� + �������� % 12) �������� �����, ����� 12 ������, ������� ((���. ����� + �������� -1) % 12)+1
        # ���. ��� ������������� �� 1, ����� ����, ��� ����� ���������� 1, ������� ���. ��� + ((�������� -1) // 12)
        return f"{(self.month + offset - 1) % 12 + 1}.{self.year + (self.month + offset - 1) // 12}"


TAG_NAMES = ["date", "DTPV", "district", "street", "house", "time", "kartId", "COORD_L", "COORD_W", "k_ul", "km", "m",
             "KTS", "KUCH", "POG", "RAN", "sdor", "spog", "osv", "factor", "ndu", "OBJ_DTP", "s_pch"]
# ������ ��� ����
TRANSLATION = {'date': '����', 'DTPV': '��� ���', 'district': '�����', 'street': '�����', 'house': '���',
               'time': '�����', 'kartId': '�����', 'COORD_L': '�������', 'COORD_W': '������', 'k_ul': '������',
               'km': '��������', 'm': '����', 'KTS': '���������� ������������ �������', 'KUCH': '���������� ����������',
               'POG': '�������', 'RAN': '������', 'sdor': '��������� ������', 'spog': '��������� ������',
               'osv': '���������', 'factor': '�������',
               'ndu1': '���������� �����������-����������������� ���������� ������-�������� ����1',
               'ndu2': '���������� �����������-����������������� ���������� ������-�������� ����2',
               'ndu3': '���������� �����������-����������������� ���������� ������-�������� ����3',
               'OBJ_DTP1': '������� ��� ������ ����� ���1', 'OBJ_DTP2': '������� ��� ������ ����� ���2',
               'OBJ_DTP3': '������� ��� ������ ����� ���3', 'OBJ_DTP4': '������� ��� ������ ����� ���4',
               'OBJ_DTP5': '������� ��� ������ ����� ���5', 'OBJ_DTP6': '������� ��� ������ ����� ���6',
               's_pch': '��������� �������� �����'}
# ������� � ���� �� �������, ��������, ��� ��� ��������� ��� ����� �����������
MULTIPLE_VALUES = ['OBJ_DTP', 'ndu']  # ��, ��� ��������� �� �����������

REGIONS = {'��������� �����': 92213, "�������� �����": 92218, "��������� �����": 92252}
FIRST_REQUEST_URL = "http://stat.gibdd.ru/map/getDTPCardDataXML"
SECOND_REQUEST_URL = 'http://stat.gibdd.ru/getPDFbyId?data='


def save_to_excel(district: str, data: Dict[str, List[str]]) -> None:
    """
    ��������� � ������

    :param district: �������� ������ �����
    :param data: ������ � �������� ���
    :return:
    """
    address = f'{district}\������ �������� ���.xml'
    tree = ET.parse(address)
    root = tree.getroot()
    read_xml(root, data)
    DataFrame(data).to_excel(f"{district}.xlsx", index=False)


def read_xml(xml, dtp_data):
    dict_for_multiple_values = dict(zip(MULTIPLE_VALUES, [0] * len(
        MULTIPLE_VALUES)))  # {'OBJ_DTP':0 , 'ndu':0} ��� ��� ������������� ��������, �������� OBJ_DTP1,OBJ_DTP2
    for child in xml:  # �������� �� ���� �����
        if len(child):  # ���� � ������� ���� �������
            if child.tag == "tab":  # ��� ��� � � ����� ���
                for key, value in dtp_data.items():  # ��������� ��� ������ " ", �.�. ��������� ���� ����� �� ����������
                    dtp_data[key].append("")
            read_xml(child, dtp_data)  # �������� �� ��� �����
        else:  # � ������� ��� �����
            if child.tag in TAG_NAMES:  # ���� ��� ���, ������� �� ����
                if child.tag in MULTIPLE_VALUES:  # ���� �� ���� �� ���, ��� ����������� ��������� ��� � ����� �������
                    dict_for_multiple_values[
                        child.tag] += 1  # ����������� �� 1 �����, ������� �� ��� �������� ������(�.�. �� ���������)
                    count = dict_for_multiple_values[
                        child.tag]  # ����� �����, �� ��� ��� ���� (������ ���, ����� ��� ����� ������� �������)
                    dtp_data[TRANSLATION[f'{child.tag}{count}']][
                        -1] = child.text  # ����������� ��� ������ �����, ������� �� �� �����
                else:
                    dtp_data[TRANSLATION[child.tag]][
                        -1] = child.text  # ���� ���� �� �� MULTIPLE_VALUES, ������ ������ ����� �� ����� �����


def get_files_id(region: str, start_date, end_date):  # ������� ��������� � �������� ����

    months = [f'"MONTHS:{start_date + offset}"' for offset in
              range(end_date - start_date)]  # ������: ["MONTHS:12.2021", "MONTHS:1.2022"]
    data = {"data": '{"date":[' + ', '.join(months) + '],' +
                    '"ParReg":"92",' +
                    '"order":{"type":"1","fieldName":"dat"},' +
                    f'"reg":"{REGIONS[region]}",' +
                    '"ind":"1","st":"1","en":"7"}'}
    
    print(data)

    reqnomer = requests.post(FIRST_REQUEST_URL, data=json.dumps(data), headers={'Content-type': 'application/json'})
    result_of_first = reqnomer.json()
    result_of_first["data"] = int(result_of_first["data"])
    reqxml = requests.get(SECOND_REQUEST_URL + str(result_of_first["data"]))
    file = zipfile.ZipFile(BytesIO(reqxml.content))
    file.extractall(district)


for district, id in REGIONS.items():
    start_date = Date("1.2021")  # ��������� ����
    end_date = Date("12.2021")  # �������� ����
    print(f'Downloading {district}')
    get_files_id(district, start_date, end_date)
    data = {}
    print(f'{district} downloaded successfully')
    print(f'Saving {district} to excel')
    for key, value in TRANSLATION.items():
        data[value] = []
    save_to_excel(district, data)
    print(f'{district} saved successfully')
print(None)