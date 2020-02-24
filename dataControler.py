from extraDataControler import ContractData
from extraModelFunc import parseRequest, parseResposne


def getDataContract(fileObj: dict, contextParams: str, contextPath: str):
    """
    Функция считывает словарь с данными контракта
    :return: выбранный тип параметров (по-умолчанию - все)
    """
    contrData = ContractData(data=fileObj)
    if contextParams == 'Request':
        parseRequest(contrData, contextPath=contextPath)
        return contrData.allRequestParams
    elif contextParams == 'Response':
        parseResposne(contrData, contextPath=contextPath)
        return contrData.allResponseParams
    else:
        parseRequest(contrData, contextPath=contextPath)
        parseResposne(contrData, contextPath=contextPath)
    return contrData.allRequestParams + contrData.allResponseParams
