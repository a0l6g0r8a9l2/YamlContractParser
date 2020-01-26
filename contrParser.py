from __future__ import annotations

from yamlParser import ContractData


def parseRequest(contrObj: ContractData):
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    msgType = 'Request'
    for subPath, parsms in contrObj.data['paths'].items():
        for item in parsms.values():
            methodName = item['operationId']
            if 'parameters' in item.keys():  # not empty request
                for dictElems in item['parameters']:
                    if 'schema' not in dictElems:
                        rootSearch(dictElems, methodName, msgType=msgType, contrObj=contrObj)
                    else:  # функция поиска в schema def
                        if '$ref' in dictElems['schema']:
                            definSearch(dictElems['schema'], method=methodName, msgType=msgType, contrObj=contrObj)
                        else:  # 'properties'
                            propSearch(dictElems['schema'], method=methodName, msgType=msgType, contrObj=contrObj)
            else:  # empty request
                contrObj.allRequestParams.append((methodName + msgType + '/', None, None))


def parseResposne(contrObj: ContractData):
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    msgType = 'Response'
    for subPath, parsms in contrObj.data['paths'].items():
        for item in parsms.values():
            methodName = item['operationId']
            if 'responses' in item.keys():  # not empty Response
                for keys, vals in item['responses'].items():
                    if keys == '200':
                        if 'schema' not in vals:
                            contrObj.allResponseParams.append((methodName + msgType + '/', None, None))
                        else:  # функция поиска в schema def
                            if '$ref' in vals['schema']:
                                definSearch(vals['schema'], method=methodName, msgType=msgType, contrObj=contrObj)
                            else:  # 'properties'
                                vals['schema'].pop('type')
                                rootSearch(vals['schema'], method=methodName, msgType=msgType, contrObj=contrObj)


def rootSearch(dictObj: dict, method: str, msgType: str = 'Request',
               contrObj: ContractData = None):
    """
    name, type def
    :param contrObj: class с данными контракта
    :param msgType: тип сообщения
    :param dictObj: словарь из списка parameters
    :param method: operationId
    :return: список кортежей из:
        метод/
        имя параметра
        тип параметра
    """
    for items in dictObj.keys():
        if items == 'items' and '$ref' in dictObj['items']:
            definSearch(dictObj['items'], method=method, msgType=msgType, contrObj=contrObj)
        elif 'properties' in dictObj.keys():  # and '$ref' in items.keys():
            propSearch(dictObj, method=method, msgType=msgType, contrObj=contrObj)
        else:
            nameParamIn, typeParamIn = method + msgType + '/' + dictObj['name'], dictObj['type']
            if msgType == 'Request':
                return contrObj.allRequestParams.append((nameParamIn, typeParamIn))
            else:
                return contrObj.allResponseParams.append((nameParamIn, typeParamIn))


def propSearch(obj: dict, nestedCollection: str = '', method: str = '', msgType: str = 'Request',
               contrObj: ContractData = None):
    """
    serch in 'properties'
    :param contrObj: class с данными контракта
    :param obj:словарь в 'properties'
    :param nestedCollection: вложенная коллекция
    :param method: имя метода
    :param msgType: тип сообщения
    :return:
    """
    if 'properties' in obj.keys():
        for keys, values in obj['properties'].items():
            if keys != 'items':
                nameParam, typeParam = method + msgType + '/' + nestedCollection + keys, values['type']
                if msgType == 'Request':
                    contrObj.allRequestParams.append((nameParam, typeParam))
                else:
                    contrObj.allResponseParams.append((nameParam, typeParam))
            else:
                rootSearch(obj['properties'], method=method, msgType=msgType, contrObj=contrObj)


def definSearch(obj: dict, nestedCollection: str = '', method: str = '', msgType: str = 'Request',
                contrObj: ContractData = None):
    """
    defenition def
    :param contrObj: class с данными контракта
    :param obj: словарь объекта definitions
    :param nestedCollection: вложенная коллекция (другой объект в defenition)
    :param method: имя метода
    :param msgType: тип сообщения
    :return: None (добавляет кортежи с параметрами в нужный словарь)
    """
    if 'items' in obj.keys() and '$ref' in obj['items']:
        definNode, defineNodeName = obj['items']['$ref'].split('/')[1:3]
        for dkeys, ditems in contrObj.data[definNode][defineNodeName]['properties'].items():
            nameParam, typeParam = method + msgType + '/' + nestedCollection + dkeys, ditems['type']  # параметры
            if msgType == 'Request':
                contrObj.allRequestParams.append((nameParam, typeParam))
            else:
                contrObj.allResponseParams.append((nameParam, typeParam))
    elif '$ref' in obj.keys():
        definNode, defineNodeName = obj['$ref'].split('/')[1:3]
        for dkeys, ditems in contrObj.data[definNode][defineNodeName]['properties'].items():
            if 'items' in ditems:  # and ditems['type'] == 'array'
                nestedCollection = dkeys + '/'
                definSearch(ditems, nestedCollection=nestedCollection, method=method, msgType=msgType, contrObj=contrObj)
            else:
                nameParam, typeParam = method + msgType + '/' + nestedCollection + dkeys, ditems['type']  # параметры
                if msgType == 'Request':
                    contrObj.allRequestParams.append((nameParam, typeParam))
                else:
                    contrObj.allResponseParams.append((nameParam, typeParam))
