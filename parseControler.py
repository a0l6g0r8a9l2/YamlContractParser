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
