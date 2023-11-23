from IND_STRATEGIES.ind_1 import HEIKEN_ASHI_PATTERN
from IND_STRATEGIES.ind_2 import BB_DOJI_ENGULGING_PATTERN

class SL_STRATEGY_ONE(BB_DOJI_ENGULGING_PATTERN, HEIKEN_ASHI_PATTERN):

    def __init__(self) -> None:
        super().__init__()

    def sl_generator_one(self, data):
        SLSignal = [0] * len(data)
        SLbackcandles = 1

        for row in range(SLbackcandles, len(data)):
            mi = 1e10
            ma = -1e10
            if data['ordersignal'].iloc[row] == 1:
                for i in range(row - SLbackcandles, row + 1):
                    ma = max(ma, data['High'].iloc[i])
                SLSignal[row] = ma

            if data['ordersignal'].iloc[row] == 2:
                for i in range(row - SLbackcandles, row + 1):
                    mi = min(mi, data['Low'].iloc[i])
                SLSignal[row] = mi

        data.loc[:, 'SLSignal'] = SLSignal
        return data
