import yaml
import pprint as pp
from dataclasses import dataclass
import pandas as pd


# TODO: Сейчас выводятся обрбатываются вх. параметры. Добавить исходящие.
#  Добавить в анализ словарь definitions -> responses (матчить из path)


def getDataContract():
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    with open(r'C:\Users\Алексей\Documents\example_yaml\FinancialInstrument v1.15.yaml', 'rt', encoding='utf-8') as ya:
        contract = ya.read()
    data = yaml.safe_load(contract)
    return data


# pp.pprint(data['basePath'])
# pp.pprint(data['host'])


@dataclass
class Path:
    subPath: str


@dataclass
class Method(Path):
    path: list
    # methodType: str
    methodName: list


@dataclass
class Params(Method):
    paramName: list
    paramDiscrip: list
    paramType: list


pathList = []
for subPath, parsms in getDataContract()['paths'].items():
    # subPaths.append(subPath)  # путь до метода
    for item in parsms.values():
        # print("methodName: " + item['operationId'], end='\n')  # метод
        for keys, vals in item.items():
            if keys == 'parameters':
                for items in vals:
                    if 'schema' not in items.keys():  # если нет ключа "schema" значит. вх. параметры ищем в
                        # parameters, инчае в "definitions"
                        nameParamIn, typeParamIn = items['name'], items['type']  # вх. параметры
                        # print(nameParamIn, typeParamIn, end='\n')
                        itemPathList = (item['operationId'] + 'Request' + '/' + nameParamIn, typeParamIn)
                        pathList.append(itemPathList)
print(pathList)
# df = pd.DataFrame(data) export_excel = df.to_excel(
# r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx', index=None, header=False)

# TODO: добавить вывод в excel построчно

# parametrs = Params(getDataContract()['basePath'], path=subPaths, methodName=methodNames,
#                    paramName=pamNames, paramDiscrip=paramDescrip, paramType=pamTypes)
# print(parametrs.subPath + parametrs.path[1] + '/' + parametrs.paramName[1])
