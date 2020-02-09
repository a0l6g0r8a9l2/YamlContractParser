from contrParser import parseRequest
from parseControler import ContractData


def getDataContract(fileObj: dict):
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    contrData = ContractData(data=fileObj)
    parseRequest(contrData)
    # parseResposne(contrData)
    print(contrData.allRequestParams)
    return contrData.allRequestParams
