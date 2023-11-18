from backtesting import Strategy, Backtest
import numpy as np
from INDS.inds import indss



class MyCandlesStrat(Strategy):
    sltr = 1
    mysize = 0.1
    def init(self):
        super().init()
        self.signal1 = self.I(indss.SIGNAL)

    # def SIGNAL(self):        
    #     return self.df.ordersignal

    def next(self):
        super().next()
        sltr = self.sltr
        for trade in self.trades: 
            if trade.is_long: 
                trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
            else:
                trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr) 

        if self.signal1==2 and len(self.trades)==0:
            self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
            sl1 = self.data.Close[-1] - self.sltr
            self.buy(sl=sl1, size=self.mysize)
        elif self.signal1==1 and len(self.trades)==0:
            self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
            sl1 = self.data.Close[-1] + self.sltr
            self.sell(sl=sl1, size=self.mysize)

def main_bt(dfpl):
    

    bt = Backtest(dfpl, MyCandlesStrat, cash=10000, margin=1/50, commission=.00)
    stat = bt.run()
    stat