from contrParser import parseRequest, parseResposne
from parseControler import ContractData


def getDataContract(fileObj: dict, context: str):
    """
    Функция считывает словарь с данными контракта
    :return: выбранный тип параметров (по-умолчанию - все)
    """
    contrData = ContractData(data=fileObj)
    if context == 'Request':
        parseRequest(contrData)
        return contrData.allRequestParams
    elif context == 'Response':
        parseResposne(contrData)
        return contrData.allResponseParams
    else:
        parseRequest(contrData)
        parseResposne(contrData)
    return contrData.allRequestParams + contrData.allResponseParams
