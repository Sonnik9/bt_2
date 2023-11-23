import pandas as pd
import numpy as np
from API_YF.yf_data import GETT_HISTORICAL_DATA
from backtesting import Strategy, Backtest
from IND_STRATEGIES.ind_1 import HEIKEN_ASHI_PATTERN
from IND_STRATEGIES.ind_2 import BB_DOJI_ENGULGING_PATTERN
import pandas_ta as ta
from SL_STRATEGYES.sl_1 import SL_STRATEGY_ONE
# from finta import TA
# import math

class MAIN_INIT(SL_STRATEGY_ONE, GETT_HISTORICAL_DATA):
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
        data = self.bb_calculator(data)
        # data = self.bollinger_doji_signal(data)
        
        # data = self.bollinger_engulfing_signal(data)
        data = self.bollinger_doji_total_signal(data)
        
        # data = self.bollinger_engulfing_total_signal(data)
        # data = self.HeikenPreparators(data)
        data = data[data.Open != data.Close]        
        # data = self.HeikenSignal1(data)
        data = self.totalSignal_2(data)
        # print(data)
        data.dropna(inplace=True)       
        # data['pointpos'] = data.apply(lambda row: self.pointpos(row), axis=1)
        data = self.sl_generator_one(data)
        self.dfpl = data[slicee:]

    def SIGNAL(self):        
        return self.dfpl['ordersignal']

def main(symbol, slicee):
    mainn_init = MAIN_INIT()
    mainn_init.go_(symbol, slicee)

    class MyCandlesStrat(Strategy):
        # sltr = 1.5
        # mysize = 0.01
        initsize = 0.01
        mysize = initsize


# original strategy 2:
# ////////////////////////////////////////////////////////////////////////
        # def init(self):
        #     super().init()
        #     self.signal1 = self.I(mainn_init.SIGNAL)
        # def next(self):
        #     super().next()
        #     TPSLRatio = 1.5

        #     if self.signal1==2 and len(self.trades)==0:   
        #         # print('buy')
        #         sl1 = min(self.data.Low[-2], self.data.Low[-1])
        #         tp1 = self.data.Close[-1] + abs(self.data.Close[-1]-sl1)*TPSLRatio
        #         self.buy(sl=sl1, tp=tp1, size=self.mysize)
            
        #     elif self.signal1==1 and len(self.trades)==0:   
        #         print('sell')      
        #         sl1 = max(self.data.High[-2], self.data.High[-1])
        #         tp1 = self.data.Close[-1] - abs(sl1-self.data.Close[-1])*TPSLRatio
        #         self.sell(sl=sl1, tp=tp1, size=self.mysize)

# /////////////////////////////////////////////////////////////////////////

# original strategy:
# /////////////////////////////////////////////////////////////////////////
        def init(self):
            super().init()
            self.signal1 = self.I(mainn_init.SIGNAL)

        def next(self):
            super().next()
            self.sltr = 1.5
            self.tp_multipliter = 1.2
            self.mysize = 0.01

            for trade in self.trades:
                # pass
                if trade.is_long:
                    trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
                else:
                    trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr)

            if self.signal1[-1] == 2 and len(self.trades) == 0:
                # print(f"long_sl: {self.data.SLSignal[-1]}")
                self.sltr = abs(self.data.Close[-1] - self.data.SLSignal[-1])
                sl1 = self.data.Close[-1] - self.sltr
                # tp1 = self.data.Close[-1] + (self.sltr*self.tp_multipliter)
                self.buy(sl=sl1, size=self.mysize)

            elif self.signal1[-1] == 1 and len(self.trades) == 0:
                # print(f"short_sl: {self.data.SLSignal[-1]}")
                self.sltr = abs(self.data.SLSignal[-1] - self.data.Close[-1])
                sl1 = self.data.Close[-1] + self.sltr
                # tp1 = self.data.Close[-1] - (self.sltr*self.tp_multipliter)
                try:
                    self.sell(sl=sl1, size=self.mysize)
                except:
                    pass
# /////////////////////////////////////////////////////////////////////////

# my atr_sl strategy/////////

        # def init(self):
        #     super().init()
        #     self.signal1 = self.I(mainn_init.SIGNAL)

        # def next(self):
        #     super().next()
        #     self.mysize = 0.01

        #     for trade in self.trades:
        #         pass

        #     if self.signal1[-1] == 2 and len(self.trades) == 0: 
        #         sl_level, tp_level = self.sl_tp_calculations(self.data, direction=2)
        #         try:
        #             if sl_level != 0 and tp_level != 0:
        #                 self.buy(sl=sl_level, tp=tp_level, size=self.mysize)
        #         except Exception as ex:
        #             print(ex)
        #     elif self.signal1[-1] == 1 and len(self.trades) == 0:
        #         sl_level, tp_level = self.sl_tp_calculations(self.data, direction=1)
        #         try:
        #             if sl_level != 0 and tp_level != 0:
        #                 self.sell(sl=sl_level, tp=tp_level, size=self.mysize)
        #         except Exception as ex:
        #             print(ex)

        # def calculate_atr(self, data, period=14):
        #     true_ranges = []
        #     for i in range(1, len(data)):
        #         high = data['High'][i]
        #         low = data['Low'][i]
        #         close = data['Close'][i - 1]
        #         true_range = max(abs(high - low), abs(high - close), abs(low - close))        
        #         true_ranges.append(true_range)
        #     atr = sum(true_ranges[-period:]) / period

        #     return atr

        # def sl_tp_calculations(self, data, direction):
        #     sl, tp = None, None
        #     atr = self.calculate_atr(data)
        #     l_pr = data['Close'][-1]
        #     # 0.9 1.2
        #     # 1 1.382
        #     # 1 1.618
        #     if direction == 2:
        #         tp, sl = l_pr + atr*1.382, l_pr - atr*1
        #         # print(f"sl_L_level: {sl}, close_price: {l_pr}, tp_L_level: {tp}")
        #         if sl >= tp or tp <= l_pr or sl >= l_pr:
        #             raise ValueError("For a long order, SL should be less than TP.")         

        #     elif direction == 1:
        #         sl, tp = l_pr + atr*1, l_pr - atr*1.382
        #         # print(f"sl_S_level: {sl}, close_price: {l_pr}, tp_S_level: {tp}")
        #         if sl <= tp or tp >= l_pr or sl <= l_pr:
        #             raise ValueError("For a long order, SL should be less than TP.")  
            
        #     return sl, tp


    
    mainn_init.dfpl.index = pd.to_datetime(mainn_init.dfpl['Date'])
    mainn_init.dfpl.drop(['Date'], axis=1, inplace=True)
    print(mainn_init.dfpl)

    bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=100000, margin=1/50, commission=0.0)
    stat = bt.run()
    print(stat)

if __name__ == "__main__":
    symbol = '^RUI'
    symbol = 'BTC-USD'
    symbol = 'ETH-USD'
    # symbol = 'SOLA-USD'
    slicee = 0
    main(symbol, slicee)
