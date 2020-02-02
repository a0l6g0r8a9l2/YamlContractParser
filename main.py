from os import path as p

import yaml
from colorama import Fore, Style, init

from contrParser import parseRequest, parseResposne
from parseControler import ContractData


def getDataContract():
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    init()
    print(Fore.GREEN, Style.DIM +
          """
    Dumb contraract path parser based on Swagger Open API Specification.
    https://swagger.io/docs/specification/
    Return list like: "operationId/../parametrName, parametrType" in Excel""")
    path = str(input("""
    Input absolute path to file : \n"""))
    if p.isfile(path):
        with open(path, 'rt', encoding='utf-8') as ya:
            contract = ya.read()
        data = yaml.safe_load(contract)
        contrData = ContractData(data=data)
        parseRequest(contrData)
        parseResposne(contrData)
        contrData.ViewAsExcel()
    else:
        return print("Указанный путь не корректен!")


getDataContract()
