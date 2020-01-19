import yaml


def getDataContract():
    """
    Функция считывает yaml
    :return: все данные контракта в объекте
    """
    with open(r'C:\Users\Алексей\Documents\example_yaml\FinancialInstrument v1.15.yaml', 'rt', encoding='utf-8') as ya:
        contract = ya.read()
    data = yaml.safe_load(contract)
    return data


def parsePathsNode():
    """
    Функция парсит ноду 'paths' в контракте
    :return: список кортежей из:
        - имя метода (operationId)
        - нода (dict) с вх. параметрами или None
        - нода (dict) c исх. пареметрами (responses)
    """
    listPathItems = []
    for subPath, parsms in getDataContract()['paths'].items():
        # subPaths.append(subPath)  # путь до метода
        for item in parsms.values():
            if 'parameters' in item.keys():
                # print('No params in: ',  item)
                methodName, parameters, responses = item['operationId'], item['parameters'], item['responses']
            else:
                methodName, parameters, responses = item['operationId'], None, item['responses']
                # print('Has params in: ', item)
            listPathItems.append((methodName, parameters, responses))
    return listPathItems


def getParamsIn():
    """
    Функция возвращет вх. параметры используя parsePathsNode ()
    :return: список кортежей из:
        - метод/параметр
        - тип параметра
    """
    # TODO: добавить обязательность параметра в вывод
    listPathItemsIn = parsePathsNode()
    paramInList = []
    msgType = 'Request'
    nodeSchemaName = 'schema'
    for items in listPathItemsIn:
        if items[1] is not None:
            for childItems in items[1]:
                if 'schema' not in childItems.keys():  # если нет ключа "schema" значит. вх. параметры ищем в
                    # parameters, инчае в "definitions"
                    nameParamIn, typeParamIn = childItems['name'], childItems['type']  # вх. параметры
                    itemParmInList = (items[0] + msgType + '/' + nameParamIn, typeParamIn)
                    paramInList.append(itemParmInList)
                else:  # ветка с поиcком в "definitions"
                    if '$ref' in childItems['schema'].keys():
                        definNode, defineNodeName = childItems['schema']['$ref'].split('/')[1:3]  # нода и наименвание
                        # объекта в которых нужно искать
                        for dkeys, ditems in getDataContract()[definNode][defineNodeName]['properties'].items():
                            nameParamIn, typeParamIn = dkeys, ditems['type']  # вх. параметры
                            itemParmInList = (items[0] + msgType + '/' + nameParamIn, typeParamIn)
                            paramInList.append(itemParmInList)
                    else:
                        for dkeys, ditems in childItems['schema']['properties'].items():
                            nameParamIn, typeParamIn = dkeys, ditems['type']
                            itemParmInList = (items[0] + msgType + '/' + nameParamIn, typeParamIn)
                            paramInList.append(itemParmInList)
    return paramInList


def getParamsOut():
    """
    Функция возвращет исх. параметры используя parsePathsNode ()
    :return: список кортежей из:
        - метод/параметр
        - тип параметра
    """
    # TODO: добавить обязательность параметра в вывод
    listPathItemsOut = parsePathsNode()
    paramOutList = []
    msgType = 'Response'
    nodeSchemaName = 'schema'
    for items in listPathItemsOut:
        for keys, vals in items[2].items():
            if keys == '200':
                if 'schema' not in vals.keys():  # если нет ключа "schema" значит. исх. параметры ищем в
                    # nameParamOut, typeParamOut = vals['name'], vals['type']  # вх. параметры
                    # paramOutList = (items[0] + msgType + '/' + nameParamOut, typeParamOut)
                    # paramOutList.append(paramOutList)
                    pass
                elif 'items' not in vals['schema'].keys():  # ветка с поиcком в "definitions"
                    # TODO: bug? в BrokerAssetRateHistory (definitions) есть параметры и в 'properties' и items, для вложенных объектов
                    if '$ref' in vals['schema'].keys():
                        print(items[0])
                        for itemsSearch in searchInDefinitions(vals, node=nodeSchemaName, msgType=msgType):
                            print(itemsSearch)
                            itemParmOutList = (items[0] + msgType + '/' + itemsSearch[0], itemsSearch[1])
                            paramOutList.append(itemParmOutList)
                    else:
                        if 'properties' in vals['schema'].keys():
                            for dkeys, ditems in vals['schema']['properties'].items():
                                nameParam, typeParam = dkeys, ditems['type']  # параметры
                                itemParmOutList = (items[0] + msgType + '/' + nameParam, typeParam)
                                paramOutList.append(itemParmOutList)
                else:
                    for itemsSearch in searchInDefinitions(vals['schema'], node='items', msgType=msgType):
                        itemParmOutList = (items[0] + msgType + '/' + itemsSearch[0], itemsSearch[1])
                        paramOutList.append(itemParmOutList)
    return paramOutList


def searchInDefinitions(vals, node='schema', msgType='Response', itemParmList=[], nameItemNode=''):
    """
    Рекурсивная функция для обработки ноды "definitions" (в т.ч.вложенных элементов)
    :param vals: словарь для поиска параметров
    :param node: schema/items
    :param msgType: request/response
    :param itemParmList: список уже полученных параметров
    :param nameItemNode: наименование вложенной коллекции
    :return: список кортежей из:
        - метод/параметр
        - тип параметра
    """
    if '$ref' in vals[node].keys():  # вместо schema - items, для вложенных объектов
        definNode, defineNodeName = vals[node]['$ref'].split('/')[1:3]  # нода и наименвание
        # объекта в которых нужно искать
        for dkeys, ditems in getDataContract()[definNode][defineNodeName]['properties'].items():
            if 'items' in ditems:  # and ditems['type'] == 'array'
                nameItemNode = dkeys + '/'
                listSerchItems = searchInDefinitions(ditems, 'items', itemParmList=itemParmList, nameItemNode=nameItemNode)
                for singlItem in listSerchItems:
                    nameParam, typeParam = nameItemNode + singlItem[0], singlItem[1]
                    itemParmList.append((nameParam, typeParam))
            else:
                nameParam, typeParam = nameItemNode + dkeys, ditems['type']  # параметры
                itemParmList.append((nameParam, typeParam))
    # elif 'properties' in vals[node].keys():
    #     for dkeys, ditems in vals[node]['properties'].items():
    #         nameParam, typeParam = nameItemNode + dkeys, ditems['type']  # параметры
    #         itemParmList.append((nameParam, typeParam))
    # else:
    #     if 'items' in vals[node]:
    #         # print(vals[node].keys())
    #         searchInDefinitions(vals[node], 'items')
    return itemParmList


# for i in getParamsIn():
#     print(i)
#
# for j in getParamsOut():
#     print(j)
# pp.pprint(parsePathsNode())

# pp.pprint(paramInList)
# df = pd.DataFrame(data) export_excel = df.to_excel(
# r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx', index=None, header=False)

# TODO: добавить вывод в excel построчно

# parametrs = Params(getDataContract()['basePath'], path=subPaths, methodName=methodNames,
#                    paramName=pamNames, paramDiscrip=paramDescrip, paramType=pamTypes)
# print(parametrs.subPath + parametrs.path[1] + '/' + parametrs.paramName[1])
