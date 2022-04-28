import zipfile
from io import BytesIO
import pandas

name_list=["date","DTPV","district","street","house","time","kartId","COORD_L","COORD_W","k_ul","km","m","KTS","KUCH","POG","RAN","sdor","spog","osv","factor","ndu","OBJ_DTP","s_pch"]

name_list_dict={'date': 'дата', 'DTPV': 'вид дтп', 'district': 'место', 'street': 'улица', 'house': 'дом', 'time': 'время', 'kartId': 'номер', 'COORD_L': 'долгота', 'COORD_W': 'широта', 'k_ul': 'дорога', 'km': 'километр', 'm': 'метр', 'KTS': 'количество транспортных средств', 'KUCH': 'количество участников', 'POG': 'погибло', 'RAN': 'ранены', 'sdor': 'состояние дороги', 'spog': 'состояние погоды', 'osv': 'освещение', 'factor': 'факторы', 'ndu1': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети1','ndu2': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети2','ndu3': 'Недостатки транспортно-эксплуатационного содержания улично-дорожной сети3', 'OBJ_DTP1': 'Объекты УДС вблизи места ДТП1','OBJ_DTP2': 'Объекты УДС вблизи места ДТП2','OBJ_DTP3': 'Объекты УДС вблизи места ДТП3','OBJ_DTP4': 'Объекты УДС вблизи места ДТП4','OBJ_DTP5': 'Объекты УДС вблизи места ДТП5','OBJ_DTP6': 'Объекты УДС вблизи места ДТП6', 's_pch': 'состояние проезжей части'}

multiple_values=['OBJ_DTP','ndu']


def read(xml):
    global data,name_list, multiple_values
    dict_for_multiple_values= {'OBJ_DTP':0,'ndu':0}
    for child in xml:
        if len(child):
            if child.tag=="tab":
                for key, value in data.items():
                    data[key].append("")
            read(child)
        else:
            if child.tag in name_list:
                if child.tag in multiple_values:
                    dict_for_multiple_values[child.tag]+=1
                    count=dict_for_multiple_values[child.tag]
                    data[name_list_dict[f'{child.tag}{count}']][-1]=child.text
                else:
                    data[name_list_dict[child.tag]][-1] = child.text

                    import xml.etree.ElementTree as ET


def toExcel(district):
    adress = f'{district}\Список карточек ДТП.xml'
    tree = ET.parse(adress)
    root = tree.getroot()
    data = {"Номер": [], "Вид ДТП": [], "Дата": [], "Место": [], "Время": []}
    read(root, data)
    df = pandas.DataFrame(data)
    df.to_excel(f"{district}.xlsx")
    #удалено "index = False" c предшествующей строки
    
