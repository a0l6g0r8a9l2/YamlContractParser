from os import path as p

import yaml
from colorama import Fore, Style, init

from contrParser import parseRequest, parseResposne
from yamlParser import ContractData, ContractDataViewer


def getDataContract():
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    init()
    print(Fore.GREEN, Style.DIM + """Dumb contraract path parser based on Swagger Open API Specification\n
    https://swagger.io/docs/specification/ \n
    Возвращает список вида: "operationId/../parametrName, parametrType" в excel для копипаста \n""")
    path = str(input("Введите полный путь до файла : \n"))
    if p.isfile(path):
        with open(path, 'rt', encoding='utf-8') as ya:
            contract = ya.read()
        data = yaml.safe_load(contract)
        contrData = ContractData(data=data)
        parseRequest(contrData)
        # print(contrData.allRequestParams)
        parseResposne(contrData)
        # print(contrData.allResponseParams)
        view = ContractDataViewer(allRequestParams=contrData.allRequestParams,
                                  allResponseParams=contrData.allResponseParams)
        view.ViewAsExcel()
    else:
        return print("Указанный путь не корректен!")


if __name__ == "__main__":
    getDataContract()
