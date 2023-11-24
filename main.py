import pandas as pd
import numpy as np
from API_YF.yf_data import GETT_HISTORICAL_DATA
from backtesting import Strategy, Backtest
# from IND_STRATEGIES.ind_1 import HEIKEN_ASHI_PATTERN
# from IND_STRATEGIES.ind_2 import BB_DOJI_ENGULGING_PATTERN
import pandas_ta as ta
from SL_STRATEGYES.sl_1 import SL_STRATEGY_ONE
from SL_STRATEGYES.sl_init import SL_INIT
# from finta import TA
# import math

class MAIN_INIT(SL_INIT, GETT_HISTORICAL_DATA):
    def __init__(self) -> None:
        super().__init__()
        self.dfpl = None
        # print(self.PIVOT_GENERAL_TYPE)

    # def pointpos(self, x):
    #     if x['ordersignal']==1:
    #         return x['High']+1e-4
    #     elif x['ordersignal']==2:
    #         return x['Low']-1e-4
    #     else:
    #         return np.nan
        
    def go_(self, symbol, slicee):
        data = self.get_historical_data(symbol)
        # ind strategy one ///////////////////////////////////////// 
        if self.ind_strategy == 1:
            data = self.init_heiken_pattern(data)     
        # ///////////////////////////////////////////////////////////

        #  ind strategy 2 ///////////////////////////////////////////////
        if self.ind_strategy == 2:
            data = self.init_bb_doji_eng_pattern(data)      
        self.dfpl = data[slicee:]

    def SIGNAL(self):        
        return self.dfpl['ordersignal']
        # return self.dfpl.bollinger_doji_signal

def main(symbol, slicee):
    mainn_init = MAIN_INIT()
    mainn_init.go_(symbol, slicee)

    class MyCandlesStrat(Strategy):        
        mysize = 0.01

        def init(self):
            super().init()
            self.sltr = 1.5
            self.signal1 = self.I(mainn_init.SIGNAL)

        def next(self):
            super().next()
            self.mysize = 0.01

            if mainn_init.sl_strategy == 1:
                for trade in self.trades:
                    # pass
                    if trade.is_long:
                        trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
                    else:
                        trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr)
            if self.signal1[-1] == 2 and len(self.trades) == 0:

                if mainn_init.sl_strategy == 1:
                    sl1 = mainn_init.sl_generator_one(self.data, self.signal1[-1])
                    try:
                        self.buy(sl=sl1, size=self.mysize)
                    except Exception as ex:
                        print(ex)
                if mainn_init.sl_strategy == 2:
                    sl1, tp1 = mainn_init.sl_generator_two(self.data, self.signal1[-1])
                    try:
                        self.buy(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

                if mainn_init.sl_strategy == 3:
                    sl1, tp1 = mainn_init.sl_generator_three(self.data, self.signal1[-1])
                    try:
                        self.buy(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)


            elif self.signal1[-1] == 1 and len(self.trades) == 0: 
            # if self.data.bollinger_engulfing_signal[-1] == 1 and len(self.trades) == 0:
                # print(self.data.bollinger_engulfing_signal)
                if mainn_init.sl_strategy == 1:
                    sl1 = mainn_init.sl_generator_one(self.data, self.signal1[-1])
                    try:
                        self.sell(sl=sl1, size=self.mysize)
                    except:
                        pass
                if mainn_init.sl_strategy == 2:
                    sl1, tp1 = mainn_init.sl_generator_two(self.data, self.signal1[-1])
                    try:
                        self.sell(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

                if mainn_init.sl_strategy == 3:
                    sl1, tp1 = mainn_init.sl_generator_three(self.data, self.signal1[-1])
                    try:
                        self.sell(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)
    
    mainn_init.dfpl.index = pd.to_datetime(mainn_init.dfpl['Date'])
    mainn_init.dfpl.drop(['Date'], axis=1, inplace=True)
    # print(mainn_init.dfpl)

    bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=100000, margin=1/50, commission=0.0)
    stat = bt.run()
    print(stat)

if __name__ == "__main__":
    symbol = '^RUI'
    symbol = 'BTC-USD'
    symbol = 'ETH-USD'
    symbol = "EURUSD=X"
    # symbol = 'SOLA-USD'
    slicee = 0
    main(symbol, slicee)
