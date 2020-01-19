from __future__ import annotations

from yamlParse import getDataContract


def parseRequest():
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    listPathItems = []
    msgType = 'Request'
    for subPath, parsms in getDataContract()['paths'].items():
        for item in parsms.values():
            methodName = item['operationId']
            if 'parameters' in item.keys():  # not empty request
                for dictElems in item['parameters']:
                    if 'schema' not in dictElems:
                        rootSearch(dictElems, methodName, msgType=msgType)
                    else:  # функция поиска в schema def
                        if '$ref' in dictElems['schema']:
                            definSearch(dictElems['schema'], method=methodName, msgType=msgType)
                        else:  # 'properties'
                            propSearch(dictElems['schema'], method=methodName, msgType=msgType)
            else:  # empty request
                allRequestParams.append((methodName + msgType + '/', None, None))


def parseResposne():
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    listPathItems = []
    msgType = 'Response'
    for subPath, parsms in getDataContract()['paths'].items():
        for item in parsms.values():
            methodName = item['operationId']
            if 'responses' in item.keys():  # not empty Response
                for keys, vals in item['responses'].items():
                    if keys == '200':
                        # print(keys, vals, type(vals))
                        if 'schema' not in vals:
                            allResponseParams.append((methodName + msgType + '/', None, None))
                        else:  # функция поиска в schema def
                            # print('Schema in :', vals)
                            if '$ref' in vals['schema']:
                                definSearch(vals['schema'], method=methodName, msgType=msgType)
                            else:  # 'properties'
                                vals['schema'].pop('type')
                                rootSearch(vals['schema'], method=methodName, msgType=msgType)


def rootSearch(obj: dict, method: str, msgType: str = 'Request'):
    """
    name, type def
    :param msgType: тип сообщения
    :param obj: словарь из списка parameters
    :param method: operationId
    :return: список кортежей из:
        метод/
        имя параметра
        тип параметра
    """
    for items in obj.keys():
        if items == 'items' and '$ref' in obj['items']:
            definSearch(obj['items'], method=method, msgType=msgType)
        elif 'properties' in obj.keys():  # and '$ref' in items.keys():
            propSearch(obj, method=method, msgType=msgType)
        else:
            nameParamIn, typeParamIn = method + msgType + '/' + obj['name'], obj['type']
            if msgType == 'Request':
                return allRequestParams.append((nameParamIn, typeParamIn))
            else:
                return allResponseParams.append((nameParamIn, typeParamIn))


def propSearch(obj: dict, nestedCollection: str = '', method: str = '', msgType: str = 'Request'):
    """
    serch in 'properties'
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
                    allRequestParams.append((nameParam, typeParam))
                else:
                    allResponseParams.append((nameParam, typeParam))
            else:
                rootSearch(obj['properties'], method=method, msgType=msgType)


def definSearch(obj: dict, nestedCollection: str = '', method: str = '', msgType: str = 'Request'):
    # todo: разобраться почему не паристся в путь вложенная нода
    """
    defenition def
    :param obj: словарь с ключем '$ref'
    :param nestedCollection: вложенная коллекция (другой объект в defenition)
    :param method: имя метода
    :param msgType: тип сообщения
    :return: None (добавляет кортежи с параметрами в нужный словарь)
    """
    if '$ref' in obj.keys():
        definNode, defineNodeName = obj['$ref'].split('/')[1:3]
        for dkeys, ditems in getDataContract()[definNode][defineNodeName]['properties'].items():
            if 'items' in ditems:  # and ditems['type'] == 'array'
                nestedCollection = dkeys + '/'
                definSearch(ditems, nestedCollection=nestedCollection, method=method, msgType=msgType)
            else:
                nameParam, typeParam = method + msgType + '/' + nestedCollection + dkeys, ditems['type']  # параметры
                if msgType == 'Request':
                    allRequestParams.append((nameParam, typeParam))
                else:
                    allResponseParams.append((nameParam, typeParam))


allRequestParams = []
allResponseParams = []
parseRequest()
parseResposne()
print(allRequestParams, '\n', len(allRequestParams), end='\n This was all request params \n')
print(allResponseParams, '\n', len(allResponseParams), end='\n This was all response params \n')
