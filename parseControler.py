from __future__ import annotations


class ContractData:

    def __init__(self, data: dict, allRequestParams=None, allResponseParams=None):
        if allResponseParams is None:
            allResponseParams = []
        if allRequestParams is None:
            allRequestParams = []
        self.data = data
        self.allRequestParams = allRequestParams
        self.allResponseParams = allResponseParams

    def saveParams(self, msgType: str, params: tuple):
        if msgType == 'Request':
            self.allRequestParams.append(params)
        else:
            self.allResponseParams.append(params)

    # def ViewAsExcel(self):
    #     paramList = []
    #     paramList.extend(self.allRequestParams)
    #     paramList.extend(self.allResponseParams)
    #     df = pd.DataFrame(paramList)
    #     try:
    #         df.to_excel(r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx',
    #                     index=None, header=False)
    #         print("Job is Done! Go see Excel")
    #     except ValueError:
    #         print("Some thing going wrong!", ValueError.__name__)
