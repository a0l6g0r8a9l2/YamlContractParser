from __future__ import annotations

from extraDataControler import ContractData


class CommonNodeParser:
    def __init__(self, msgType: str, methodName: str, contrObj: ContractData):
        # self.nodeObj = nodeObj
        self.msgType = msgType
        self.methodName = methodName
        self.contrObj = contrObj

    def rootSearch(self, nodeObj: dict):
        """
        name, type def
        :param nodeObj: словарь из списка parameters
        :return: список кортежей из:
            метод/
            имя параметра
            тип параметра
        """
        if nodeObj.get('items') and '$ref' in nodeObj['items']:
            self.definSearch(nodeObj['items'])
        elif 'properties' in nodeObj.keys():  # and '$ref' in items.keys():
            self.propSearch(nodeObj)
        else:
            nameParam, typeParam = self.methodName + self.msgType + '/' + nodeObj['name'], nodeObj['type']
            self.contrObj.saveParams(self.msgType, (nameParam, typeParam))

    def propSearch(self, nodeObj: dict, nestedCollection: str = ''):
        """
        serch in 'properties'
        :param nodeObj:словарь в 'properties'
        :param nestedCollection: вложенная коллекция
        :return:
        """
        if 'properties' in nodeObj.keys():
            for keys, values in nodeObj['properties'].items():
                if keys != 'items':
                    nameParam, typeParam = self.methodName + self.msgType + '/' + nestedCollection + keys, values['type']
                    self.contrObj.saveParams(self.msgType, (nameParam, typeParam))
                else:
                    self.rootSearch(nodeObj['properties'])

    def definSearch(self, nodeObj: dict, nestedCollection: str = ''):
        """
        defenition def
        :param nodeObj: словарь объекта definitions
        :param nestedCollection: вложенная коллекция (другой объект в defenition)
        :return: None (добавляет кортежи с параметрами в нужный словарь)
        """
        if 'items' in nodeObj.keys() and '$ref' in nodeObj['items']:
            definNode, defineNodeName = nodeObj['items']['$ref'].split('/')[1:3]
            for dkeys, ditems in self.contrObj.data[definNode][defineNodeName]['properties'].items():
                nameParam, typeParam = self.methodName + self.msgType + '/' + nestedCollection + dkeys, ditems['type']  # параметры
                self.contrObj.saveParams(self.msgType, (nameParam, typeParam))
        elif '$ref' in nodeObj.keys():
            definNode, defineNodeName = nodeObj['$ref'].split('/')[1:3]
            for dkeys, ditems in self.contrObj.data[definNode][defineNodeName]['properties'].items():
                if 'items' in ditems:  # and ditems['type'] == 'array'
                    nestedCollection = dkeys + '/'
                    self.definSearch(ditems, nestedCollection=nestedCollection)
                else:
                    nameParam, typeParam = self.methodName + self.msgType + '/' + nestedCollection + dkeys, ditems[
                        'type']  # параметры
                    self.contrObj.saveParams(self.msgType, (nameParam, typeParam))
