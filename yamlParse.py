import yaml
import pprint as pp
from dataclasses import dataclass
import pandas as pd


# def getPathNode():
#     """
#     Обращается к getDataContract
#     :return: нода 'paths'
#     """
#     pathNode = getDataContract()['paths']
#     # pp.pprint(data['paths'])
#     return pathNode


def getDataContract():
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    with open(r'C:\Users\Алексей\Documents\example_yaml\FinancialInstrument v1.15.yaml', 'rt', encoding='utf-8') as ya:
        contract = ya.read()
    data = yaml.safe_load(contract)
    return data


# pp.pprint(data['basePath'])
# pp.pprint(data['host'])


@dataclass
class Path:
    subPath: str


@dataclass
class Method(Path):
    path: list
    # methodType: str
    methodName: list


@dataclass
class Params(Method):
    paramName: list
    paramDiscrip: list
    paramType: list


subPaths = []
methodNames = []
pamNames = []
pamTypes = []
paramDescrip = []
for subPath, parsms in getDataContract()['paths'].items():
    print("path: " + subPath)
    subPaths.append(subPath)
    for item in parsms.values():
        print("methodName: " + item['operationId'], end='\n')
        methodNames.append(item['operationId'])
        for keys, vals in item.items():
            if keys == 'parameters':
                for items in vals:
                    if items['name']:  # items['type'], items['description']
                        print(items['name'])
                        pamNames.append(items['name'])
                    elif items['type']:
                        pamTypes.append(items['type'])
                    elif items['description']:
                        paramDescrip.append(items['description'])
            # print(type(keys), type(vals), end='\n')
            # print(keys, vals, end='\n')

# df = pd.DataFrame(data) export_excel = df.to_excel(
# r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx', index=None, header=False)

parametrs = Params(getDataContract()['basePath'], path=subPaths, methodName=methodNames,
                   paramName=pamNames, paramDiscrip=paramDescrip, paramType=pamTypes)
print(parametrs.subPath + parametrs.path[1] + '/' + parametrs.paramName[1])
