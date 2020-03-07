from baseModelFunc import CommonNodeParser as CnP
from extraDataControler import ContractData


def parseRequest(contrObj: ContractData, contextPath: str = 'operationId'):
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    msgContext = 'Request'
    msgType = 'Request'
    for subPath, parsms in contrObj.data['paths'].items():
        for item in parsms.values():
            if contextPath != 'operationId':
                methodName = subPath
                msgType = ''
            else:
                methodName = item['operationId']
            reqObj = CnP(msgType, methodName, contrObj, msgContext=msgContext)
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
                contrObj.saveParams(msgContext, (methodName + msgType + '/', None))


def parseResposne(contrObj: ContractData, contextPath: str = 'operationId'):
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:d
        - имя метода (operationId)
        - имя параметра
        - тип параметра
    """
    msgContext = 'Response'
    msgType = 'Request'
    for subPath, parsms in contrObj.data['paths'].items():
        for item in parsms.values():
            if contextPath != 'operationId':
                methodName = subPath
                msgType = ''
            else:
                methodName = item['operationId']
            resObj = CnP(msgType, methodName, contrObj, msgContext=msgContext)
            if 'responses' in item.keys():  # not empty Response
                for keys, vals in item['responses'].items():
                    if keys == '200':
                        if 'schema' not in vals:
                            contrObj.saveParams(msgContext, (methodName + msgType + '/', None))
                        else:  # функция поиска в schema def
                            if '$ref' in vals['schema']:
                                resObj.definSearch(vals['schema'])
                            else:  # 'properties'
                                vals['schema'].pop('type')
                                resObj.rootSearch(vals['schema'])
