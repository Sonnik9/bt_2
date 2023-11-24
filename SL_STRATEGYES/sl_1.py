
class SL_STRATEGY_ONE():

    def __init__(self) -> None:
        super().__init__()

    def sl_generator_one(self, data, defender):
        mi = 1e10
        ma = -1e10
        if defender == 2:               
            mi = min(mi, data['Low'][-1])
            sltr = abs(data.Close[-1] - mi)
            sl1 = data.Close[-1] - sltr
            return sl1
        if defender == 1:                
            ma = max(ma, data['High'][-1])
            sltr = abs(ma - data.Close[-1])
            sl1 = data.Close[-1] + sltr
            return sl1
        return None

    # def sl_generator_one(self, data):
    #     SLSignal = [0] * len(data)
    #     SLbackcandles = 1

    #     for row in range(SLbackcandles, len(data)):
    #         mi = 1e10
    #         ma = -1e10
    #         if data['ordersignal'].iloc[row] == 1:
    #             for i in range(row - SLbackcandles, row + 1):
    #                 ma = max(ma, data['High'].iloc[i])
    #             SLSignal[row] = ma

    #         if data['ordersignal'].iloc[row] == 2:
    #             for i in range(row - SLbackcandles, row + 1):
    #                 mi = min(mi, data['Low'].iloc[i])
    #             SLSignal[row] = mi

    #     data.loc[:, 'SLSignal'] = SLSignal
    #     return data
