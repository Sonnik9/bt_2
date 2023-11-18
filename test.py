import yfinance as yf
import pandas_ta as tafrom 
import math
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from datetime import datetime
from backtesting import Strategy
from backtesting import Backtest
import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
data = yf.download(tickers = '^RUI', start = '2012-03-11',end = '2022-07-10')
data.drop(['Volume'], axis=1, inplace=True)
data.head(10)

data['Heiken_Close'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
data['Heiken_Open'] = data['Open']
for i in range(1, len(data)):
    data['Heiken_Open'].iloc[i] = (data['Heiken_Open'].iloc[i-1] + data['Heiken_Close'].iloc[i-1]) / 2

data['Heiken_High'] = data[['High', 'Heiken_Open', 'Heiken_Close']].max(axis=1)
data['Heiken_Low'] = data[['Low', 'Heiken_Open', 'Heiken_Close']].min(axis=1)
data.dropna(inplace=True)
data.head(10)

def HeikenSignal1(df):
    signal1=[0]*len(df)
    # signal1=[0 for i in rqnge(len(df))]
    for i in range(1, len(df)):
        #df.Heiken_High[i-1]<=df.Heiken_Open[i-1])and
        PreviousHeikenBody = math.fabs(df.Heiken_Open[i-1]-df.Heiken_Close[i-1])
        ratio = 1.5
        if ( 
            (df.Heiken_High[i-1]-max(df.Heiken_Open[i-1], df.Heiken_Close[i-1]))
            /PreviousHeikenBody>ratio and
            (min(df.Heiken_Open[i-1], df.Heiken_Close[i-1]) - df.Heiken_Low[i-1])
            /PreviousHeikenBody>ratio and
            (df.Heiken_Open[i]<df.Heiken_Close[i] and df.Heiken_Low[i]>=df.Heiken_Open[i]) ):
            signal1[i]=2
        #df.Heiken_High[i-1]<=df.Heiken_Open[i-1])and
        if ( (df.Heiken_High[i-1]-max(df.Heiken_Open[i-1], df.Heiken_Close[i-1]))
            /PreviousHeikenBody>ratio>ratio and
            (min(df.Heiken_Open[i-1], df.Heiken_Close[i-1]) - df.Heiken_Low[i-1])
            /PreviousHeikenBody>ratio>ratio and
            (df.Heiken_Open[i]>df.Heiken_Close[i] and df.Heiken_High[i]<=df.Heiken_Open[i]) ):
            signal1[i]=1
    df['HeikenSignal1'] = signal1
    
def totalSignal(df):
    ordersignal=[0]*len(df)
    for i in range(0, len(df)):
        if (df.EMA10[i]>df.EMA30[i] and df.Heiken_Open[i]<df.EMA10[i] 
            and df.Heiken_Close[i]>df.EMA10[i] 
            and df.HeikenSignal1[i] == 2):
            ordersignal[i]=2
        if (df.EMA10[i]<df.EMA30[i] and df.Heiken_Open[i]>df.EMA10[i] 
            and df.Heiken_Close[i]<df.EMA10[i]
            and df.HeikenSignal1[i] == 1):
            ordersignal[i]=1
    df['ordersignal']=ordersignal
data = HeikenSignal1(data)
data = totalSignal(data)

data.dropna(inplace=True)
data.reset_index(inplace=True)
data

def pointpos(x):
    if x['ordersignal']==1:
        return x['High']+1e-4
    elif x['ordersignal']==2:
        return x['Low']-1e-4
    else:
        return np.nan
data['pointpos'] = df=data.apply(lambda row: pointpos(row), axis=1)

dfpl = data[2000:2100]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Heiken_Open'],
                high=dfpl['Heiken_High'],
                low=dfpl['Heiken_Low'],
                close=dfpl['Heiken_Close']),
                     go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
                     go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="Signal")
fig.show()

dfpl = data[2100:2200]
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),
                     go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
                     go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="Signal")
fig.show()


# StopLoss from signal
SLSignal = [0] * len(df)
SLbackcandles = 1
for row in range(SLbackcandles, len(data)):
    mi=1e10
    ma=-1e10
    if data.ordersignal[row]==1:
        for i in range(row-SLbackcandles, row+1):
            ma = max(ma,data.High[i])
        SLSignal[row]=ma
    if data.ordersignal[row]==2:
        for i in range(row-SLbackcandles, row+1):
            mi = min(mi,data.Low[i])
        SLSignal[row]=mi
        
data['SLSignal']=SLSignal

dfpl = df[:]
def SIGNAL():
    return dfpl.ordersignal


dfpl = data[:]


class MyStrat(Strategy):
    initsize = 0.2
    mysize = initsize
    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        TPSLRatio = 1
        
        #if len(self.trades)>0:            
        #    if self.trades[-1].is_long and self.data.RSI[-1]>=70:
        #        self.trades[-1].close()
        #    elif self.trades[-1].is_short and self.data.RSI[-1]<=30:
        #        self.trades[-1].close()
                   
        if len(self.trades)>0:            
            if self.trades[-1].is_long and self.data.Heiken_Open[-1]>=self.data.Heiken_Close[-1]:
                self.trades[-1].close()
            elif self.trades[-1].is_short and self.data.Heiken_Open[-1]<=self.data.Heiken_Close[-1]:
                self.trades[-1].close()
        
        if self.signal1==2 and len(self.trades)==0:   
            sl1 = self.data.SLSignal[-1]
            tp1 = self.data.Close[-1]+(self.data.Close[-1] - sl1)*TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)
        
        elif self.signal1==1 and len(self.trades)==0:         
            sl1 = self.data.SLSignal[-1]
            tp1 = self.data.Close[-1]-(sl1 - self.data.Close[-1])*TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)

bt = Backtest(dfpl, MyStrat, cash=10000, margin=1/50, commission=.00)
stat = bt.run()
stat

bt.plot(show_legend=False)


# from backtesting import Strategy, Backtest
# import numpy as np

# class MyCandlesStrat(Strategy):
#     sltr = 1
#     mysize = 0.1
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next()
#         sltr = self.sltr
#         for trade in self.trades: 
#             if trade.is_long: 
#                 trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
#             else:
#                 trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr) 

#         if self.signal1==2 and len(self.trades)==0:
#             self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
#             sl1 = self.data.Close[-1] - self.sltr
#             self.buy(sl=sl1, size=self.mysize)
#         elif self.signal1==1 and len(self.trades)==0:
#             self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
#             sl1 = self.data.Close[-1] + self.sltr
#             self.sell(sl=sl1, size=self.mysize)

# bt = Backtest(dfpl, MyCandlesStrat, cash=10000, margin=1/50, commission=.00)
# stat = bt.run()
# stat

# bt.plot(show_legend=False)
