from __future__ import annotations

from commonFunc import CommonNodeParser as Cnd
from parseControler import ContractData


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
            reqObj = Cnd(msgType, methodName, contrObj)
            if 'parameters' in item.keys():  # not empty request
                for dictElems in item['parameters']:
                    if 'schema' not in dictElems:
                        reqObj.rootSearch(dictElems)
                    else:  # функция поиска в schema def
                        if '$ref' in dictElems['schema']:
                            reqObj.definSearch(dictElems['schema'])
                        else:  # 'properties'
                            reqObj.propSearch(dictElems['schema'])
            else:  # empty request
                contrObj.saveParams(msgType, (methodName + msgType + '/', None))


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
            resObj = Cnd(msgType, methodName, contrObj)
            if 'responses' in item.keys():  # not empty Response
                for keys, vals in item['responses'].items():
                    if keys == '200':
                        if 'schema' not in vals:
                            contrObj.saveParams(msgType, (methodName + msgType + '/', None))
                        else:  # функция поиска в schema def
                            if '$ref' in vals['schema']:
                                resObj.definSearch(vals['schema'])
                            else:  # 'properties'
                                vals['schema'].pop('type')
                                resObj.rootSearch(vals['schema'])
