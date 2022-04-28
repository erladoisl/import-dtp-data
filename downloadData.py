import requests
import zipfile
import json
from io import BytesIO
import daplib
# Импортируем модуль daplib
# словарь с двумя пунктами 
global_dict = {}
# globals = dict{}
monthCounter = 0
daplib.set_params_as_variables(global_dict)  # Создается процесс считывания параметров из параметров узла


REGIONS = {'Атнинский район': 92213, "Буинский район": 92218, "Сабинский район": 92252, "г. Казань": 92401}
FIRST_REQUEST_URL = "http://stat.gibdd.ru/map/getDTPCardDataXML"
SECOND_REQUEST_URL = 'http://stat.gibdd.ru/getPDFbyId?data='


#def getFilesId(region: str, startMonth: float, endMonth: float,year: float):
#    data = {"data": '{"date":["MONTHS:2.2021","MONTHS:3.2021","MONTHS:4.2021","MONTHS:5.2021","MONTHS:12.2021"],' +
#                    '"ParReg":"92",' +
#                    '"order":{"type":"1","fieldName":"dat"},' +
#                    f'"reg":"{REGIONS[region]}",' +
#                    '"ind":"1","st":"1","en":"7"}'}

# организация генерации дат
def getFilesId(region: str, startMonth: float, endMonth: float,year: float):
    data = {"data": '{"date":' +
                        for i in range [global_dict["startMonth"], global_dict["endMonth"]]:
                                ' [MONTHS:' {monthCounter += 1}'.'{global_dict["year"]}]' +
                        '"ParReg":"92",' +
                        '"order":{"type":"1","fieldName":"dat"},' +
                        f'"reg":"{REGIONS[region]}",' +
                        '"ind":"1","st":"1","en":"7"}'}

    print('Downloading started')
    reqnomer = requests.post(FIRST_REQUEST_URL, data = json.dumps(data), headers = {'Content-type': 'application/json'})
    resultOfFirst = reqnomer.json()
    resultOfFirst["data"] = int(resultOfFirst["data"])
    reqxml = requests.get(SECOND_REQUEST_URL + str(resultOfFirst["data"]))
    file = zipfile.ZipFile(BytesIO(reqxml.content))
    file.extractall(district)
    # добавить передачу или получение параметра district # добавлено
    print("Downloading completed")


getFilesId(global_dict["region"],global_dict["startMonth"],global_dict["endMonth"], global_dict["year"])

print(global_dict)
print(data)