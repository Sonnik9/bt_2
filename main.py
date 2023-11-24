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

        if self.sl_strategy == 1:
            data = self.sl_generator_one(data)   
        self.dfpl = data

    def SIGNAL(self):        
        return self.dfpl['ordersignal']
        # return self.dfpl.bollinger_engulfing_signal

def main(symbol, slicee):
    mainn_init = MAIN_INIT()
    mainn_init.go_(symbol, slicee)

    class MyCandlesStrat(Strategy):        
        mysize = 0.01

        def init(self):
            super().init()
            self.sltr = 1.5
            self.signal1 = self.I(mainn_init.SIGNAL)

# /////////////////// 1 ////////////////////////////////////////////////

        def next(self):
            super().next()            
            TPSLRatio = 1.618

            if mainn_init.sl_strategy == 1:
                for trade in self.trades: 
                    if trade.is_long: 
                        trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
                    else:
                        trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr) 

                if self.signal1==2 and len(self.trades)==0:
                    self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
                    sl1 = self.data.Close[-1] - self.sltr
                    try:
                        self.buy(sl=sl1, size=self.mysize)
                    except Exception as ex:
                        print(ex)
                elif self.signal1==1 and len(self.trades)==0:
                    self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
                    sl1 = self.data.Close[-1] + self.sltr
                    try:
                        self.buy(sl=sl1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

            if mainn_init.sl_strategy == 2:           

                if self.signal1==2 and len(self.trades)==0:   
                    sl1, tp1 = self.sl_generator_two(self.data, self.signal1)
                    try:
                        self.buy(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

                elif self.signal1==1 and len(self.trades)==0:         
                    sl1, tp1 = self.sl_generator_two(self.data, self.signal1)
                    try:
                        self.sell(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

            if mainn_init.sl_strategy == 3:

                if self.signal1==2 and len(self.trades)==0:   
                    sl1 = min(self.data.Low[-2], self.data.Low[-1])
                    tp1 = self.data.Close[-1] + abs(self.data.Close[-1]-sl1)*TPSLRatio
                    try:
                        self.buy(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)
                
                elif self.signal1==1 and len(self.trades)==0:         
                    sl1 = max(self.data.High[-2], self.data.High[-1])
                    tp1 = self.data.Close[-1] - abs(sl1-self.data.Close[-1])*TPSLRatio
                    try:
                        self.sell(sl=sl1, tp=tp1, size=self.mysize)
                    except Exception as ex:
                        print(ex)

        def calculate_atr(self, data, period=14):
            true_ranges = []
            for i in range(1, len(data)):
                high = data['High'][i]
                low = data['Low'][i]
                close = data['Close'][i - 1]
                true_range = max(abs(high - low), abs(high - close), abs(low - close))        
                true_ranges.append(true_range)
            atr = sum(true_ranges[-period:]) / period

            return atr

        def sl_generator_two(self, data, defender):
            sl, tp = None, None
            atr = self.calculate_atr(data)
            l_pr = data['Close'][-1]
            # 0.9 1.2
            # 1 1.382
            # 1 1.618
            if defender == 2:
                tp, sl = l_pr + atr*1.618, l_pr - atr*1
                # print(f"sl_L_level: {sl}, close_price: {l_pr}, tp_L_level: {tp}")
                if sl >= tp or tp <= l_pr or sl >= l_pr:
                    raise ValueError("For a long order, SL should be less than TP.")         

            elif defender == 1:
                sl, tp = l_pr + atr*1, l_pr - atr*1.618
                # print(f"sl_S_level: {sl}, close_price: {l_pr}, tp_S_level: {tp}")
                if sl <= tp or tp >= l_pr or sl <= l_pr:
                    raise ValueError("For a long order, SL should be less than TP.")  
            
            return sl, tp
        
    mainn_init.dfpl.index = pd.to_datetime(mainn_init.dfpl['Date'])
    mainn_init.dfpl.drop(['Date'], axis=1, inplace=True)
    # print(mainn_init.dfpl)

    bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=100000, margin=1/50, commission=0.0)
    stat = bt.run()
    print(stat)

if __name__ == "__main__":
    symbol = '^RUI'
    # symbol = 'BTC-USD'
    symbol = 'ETH-USD'
    # symbol = "EURUSD=X"
    # symbol = 'SOLA-USD'
    slicee = 0
    main(symbol, slicee)
