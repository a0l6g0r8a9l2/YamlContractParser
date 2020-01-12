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


# @dataclass
# class Path:
#     subPath: str


@dataclass
class Method:
    # path: list
    # methodType: str
    methodName: list


@dataclass
class Params(Method):
    paramName: list
    paramDiscrip: list
    paramType: list


def parsePathsNode():
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - нода (dict) с вх. параметрами или None
        - нода (dict) c исх. пареметрами (responses)
    """
    listPathItems = []
    for subPath, parsms in getDataContract()['paths'].items():
        # subPaths.append(subPath)  # путь до метода
        for item in parsms.values():
            if 'parameters' in item.keys():
                # print('No params in: ',  item)
                methodName, parameters, responses = item['operationId'], item['parameters'], item['responses']
            else:
                methodName, parameters, responses = item['operationId'], None, item['responses']
                # print('Has params in: ', item)
            listPathItems.append((methodName, parameters, responses))
    return listPathItems


def getParamsIn():
    """
    Функция возвращет вх. параметры используя parsePathsNode ()
    :return: список кортежей из:
        - метод/параметр
        - тип параметра
    """
    # TODO: добавить обязательность параметра в вывод
    listPathItemsIn = parsePathsNode()
    paramInList = []
    for items in listPathItemsIn:
        if items[1] is not None:
            for childItems in items[1]:
                if 'schema' not in childItems.keys():  # если нет ключа "schema" значит. вх. параметры ищем в
                    # parameters, инчае в "definitions"
                    nameParamIn, typeParamIn = childItems['name'], childItems['type']  # вх. параметры
                    # print(nameParamIn, typeParamIn, end='\n')
                    itemParmInList = (items[0] + 'Request' + '/' + nameParamIn, typeParamIn)
                    paramInList.append(itemParmInList)
                else:  # ветка с посиком в "definitions"
                    if '$ref' in childItems['schema'].keys():
                        definNode, defineNodeName = childItems['schema']['$ref'].split('/')[1:3]  # нода и наименвание
                        # объекта в которых нужно искать
                        for dkeys, ditems in getDataContract()[definNode][defineNodeName]['properties'].items():
                            nameParamIn, typeParamIn = dkeys, ditems['type']  # вх. параметры
                            itemParmInList = (items[0] + 'Request' + '/' + nameParamIn, typeParamIn)
                            paramInList.append(itemParmInList)
    return paramInList


# TODO: Добавить обработку объектов в "definitions" содержащих ссылки на другие объекты в "definitions". Нужна рекурсия?


def getParamsOut():
    """
    Функция возвращет исх. параметры используя parsePathsNode ()
    :return: список кортежей из:
        - метод/параметр
        - тип параметра
    """
    # TODO: добавить обязательность параметра в вывод
    listPathItemsOut = parsePathsNode()
    paramOutList = []
    for items in listPathItemsOut:
        for keys, vals in items[2].items():
            if keys == '200':
                if 'schema' not in vals.keys():  # если нет ключа "schema" значит. исх. параметры ищем в
                    # parameters (?), инчае в "definitions"
                    pass  # пустой Response
                else:  # ветка с посиком в "definitions"
                    if '$ref' in vals['schema'].keys():
                        definNode, defineNodeName = vals['schema']['$ref'].split('/')[1:3]  # нода и наименвание
                        # объекта в которых нужно искать
                        for dkeys, ditems in getDataContract()[definNode][defineNodeName]['properties'].items():
                            nameParamOut, typeParamOut = dkeys, ditems['type']  # вх. параметры
                            itemParmOutList = (items[0] + 'Response' + '/' + nameParamOut, typeParamOut)
                            paramOutList.append(itemParmOutList)
    return paramOutList


for i in getParamsIn():
    print(i)

for j in getParamsOut():
    print(j)

# pp.pprint(paramInList)
# df = pd.DataFrame(data) export_excel = df.to_excel(
# r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx', index=None, header=False)

# TODO: добавить вывод в excel построчно

# parametrs = Params(getDataContract()['basePath'], path=subPaths, methodName=methodNames,
#                    paramName=pamNames, paramDiscrip=paramDescrip, paramType=pamTypes)
# print(parametrs.subPath + parametrs.path[1] + '/' + parametrs.paramName[1])
