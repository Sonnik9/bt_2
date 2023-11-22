import pandas as pd
import numpy as np
from API_YF.yf_data import GETT_HISTORICAL_DATA
from backtesting import Strategy, Backtest
from SL_STRATEGYES.sl_1 import SL_STRATEGY_ONE

class MAIN_INIT(GETT_HISTORICAL_DATA, SL_STRATEGY_ONE):
    def __init__(self) -> None:
        super().__init__()

    # def pointpos(self, x):
    #     if x['ordersignal']==1:
    #         return x['High']+1e-4
    #     elif x['ordersignal']==2:
    #         return x['Low']-1e-4
    #     else:
    #         return np.nan
        
    def go_(self, symbol, slicee):
        data = self.get_historical_data(symbol)
        data = self.HeikenPreparators(data)
        data = data[data.Open != data.Close]        
        data = self.HeikenSignal1(data)
        data = self.totalSignal(data)
        data.dropna(inplace=True)       
        # data['pointpos'] = data.apply(lambda row: self.pointpos(row), axis=1)
        self.sl_generator(data)
        self.dfpl = self.dfpl[slicee:]

    def SIGNAL(self):        
        return self.dfpl['ordersignal']

def main(symbol, slicee):
    mainn_init = MAIN_INIT()
    mainn_init.go_(symbol, slicee)

    class MyCandlesStrat(Strategy):
        sltr = 1.5
        mysize = 0.01

        def init(self):
            super().init()
            self.signal1 = self.I(mainn_init.SIGNAL)

        def next(self):
            super().next()
            self.sltr = 1.5
            self.mysize = 0.01

            for trade in self.trades:
                if trade.is_long:
                    trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
                else:
                    trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr)

            if self.signal1[-1] == 2 and len(self.trades) == 0:
                # print(f"long_sl: {self.data.SLSignal[-1]}")
                self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
                sl1 = self.data.Close[-1] - self.sltr
                self.buy(sl=sl1, size=self.mysize)

            elif self.signal1[-1] == 1 and len(self.trades) == 0:
                # print(f"short_sl: {self.data.SLSignal[-1]}")
                self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
                sl1 = self.data.Close[-1] + self.sltr
                self.sell(sl=sl1, size=self.mysize)
    
    mainn_init.dfpl.index = pd.to_datetime(mainn_init.dfpl['Date'])
    mainn_init.dfpl.drop(['Date'], axis=1, inplace=True)

    bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=100000, margin=1/50, commission=0.0)
    stat = bt.run()
    print(stat)

if __name__ == "__main__":
    symbol = '^RUI'
    # symbol = 'BTC-USDT'
    symbol = 'ETH-USD'
    slicee = 0
    main(symbol, slicee)
