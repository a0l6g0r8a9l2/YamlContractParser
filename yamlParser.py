from __future__ import annotations

import pandas as pd


class ContractData:

    def __init__(self, data: dict, allRequestParams: list = [], allResponseParams: list = []):
        self.data = data
        self.allRequestParams = allRequestParams
        self.allResponseParams = allResponseParams


class ContractDataViewer:

    def __init__(self, allRequestParams: list = [], allResponseParams: list = []):
        self.allResponseParams = allRequestParams
        self.allRequestParams = allResponseParams

    def ViewAsExcel(self):
        paramList = []
        paramList.extend(self.allRequestParams)
        paramList.extend(self.allResponseParams)
        df = pd.DataFrame(paramList)
        try:
            df.to_excel(r'C:\Users\Алексей\PycharmProjects\YamlContractParser\export_dataframe.xlsx',
                        index=None, header=False)
            print("Job is Done! Go see Excel")
        except Exception:
            print("Что-то пошло не так при сохранении в Excel")

# todo:консольный интерфейс: colorama - цветные сообщения, pyinstaller - упаковщик в exe
