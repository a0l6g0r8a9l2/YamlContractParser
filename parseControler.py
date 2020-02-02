from __future__ import annotations

import pandas as pd


class ContractData:

    def __init__(self, data: dict, allRequestParams: list = [], allResponseParams: list = []):
        self.data = data
        self.allRequestParams = allRequestParams
        self.allResponseParams = allResponseParams

    def saveParams(self, msgType: str, params: tuple):
        if msgType == 'Request':
            return self.allRequestParams.append(params)
        else:
            return self.allResponseParams.append(params)

    def ViewAsExcel(self):
        paramList = []
        paramList.extend(self.allRequestParams)
        paramList.extend(self.allResponseParams)
        df = pd.DataFrame(paramList)
        try:
            df.to_excel(r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx',
                        index=None, header=False)
            print("Job is Done! Go see Excel")
        except ValueError:
            print("Some thing going wrong!", ValueError.__name__)
