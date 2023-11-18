import math
import pandas_ta as ta
import numpy as np

class INDICATORSS():

    def __init__(self) -> None:
        self.dfpl = None

    def calc_inds(self, data):        
        data['Heiken_Close'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
        data['Heiken_Open'] = data['Open']
        for i in range(1, len(data)):
            data['Heiken_Open'].iloc[i] = (data['Heiken_Open'].iloc[i-1] + data['Heiken_Close'].iloc[i-1]) / 2

        data['Heiken_High'] = data[['High', 'Heiken_Open', 'Heiken_Close']].max(axis=1)
        data['Heiken_Low'] = data[['Low', 'Heiken_Open', 'Heiken_Close']].min(axis=1)
        data.dropna(inplace=True)
        data.head(10)

        # data["EMA20"] = ta.ema(data['Close'], length=20)
        # data["EMA50"] = ta.ema(data['Close'], length=50)
        data["EMA10"] = ta.ema(data['Close'], length=10)
        data["EMA30"] = ta.ema(data['Close'], length=30)
        data['RSI'] = ta.rsi(data['Close'], length=12)
        data.dropna(inplace=True)
        return data

    def HeikenSignal1(self, df):
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
        return df

    def totalSignal(self, df):
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
        # ordersignal_len = sum(1 for x in df['ordersignal'] if x == 2 or x == 1)
        # print(len(df))
        # print(ordersignal_len)
        # print(len(df)/ordersignal_len)
        return df
    
    def pointpos(self, x):
        if x['ordersignal']==1:
            return x['High']+1e-4
        elif x['ordersignal']==2:
            return x['Low']-1e-4
        else:
            return np.nan

    def sl_generator(self, data):
        # StopLoss from signal
        SLSignal = [0] * len(data)
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
        
        
        self.dfpl = data[500:]
        return self.dfpl

    def SIGNAL(self):        
        return self.dfpl.ordersignal
    
indss = INDICATORSS()
            

    
    # def signals_handler(self, df): 
    #     # print(df['ordersignal'])
    #     try:       
    #         if df['ordersignal'].iloc[-1] == 1:
    #             return 'BUY'
    #         elif df['ordersignal'].iloc[-1] == -1:
    #             return 'SELL'
    #         else:
    #             return 'NEUTRAL'
    #     except:        
    #         return None


