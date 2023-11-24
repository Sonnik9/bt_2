import pandas_ta as ta
from pparamss import INIT_PARAMS

class BB_DOJI_ENGULGING_PATTERN(INIT_PARAMS):
    def __init__(self) -> None: 
        super().__init__()       
        # self.dfpl = None

    def bb_calculator(self, data):        
        dataBB_382 = ta.bbands(data.Close, length=30, std=1.382) 
        dataBB_618 = ta.bbands(data.Close, length=30, std=1.618)  
        # print(dataBB_382)
        data = data.join(dataBB_382)
        data = data.join(dataBB_618)
        # data.columns
        data.dropna(inplace=True)
        # print(data)
        return data
    
    def bollinger_engulfing_signal_func(self, df): 
        #bullish signal
        if (df.Close.iloc[-1] > df['BBL_30_1.618'].iloc[-1] and df.Close.iloc[-1] < df['BBM_30_1.382'].iloc[-1] and
        df.Close.iloc[-1] > df.Open.iloc[-1] and
        df.Close.iloc[-2] < df.Open.iloc[-2] and
        df.Open.iloc[-1] < df.Close.iloc[-2] and
        df.Close.iloc[-1] > df.Open.iloc[-2] ):
            return 2
        
        #bearish signal
        elif (df.Close.iloc[-1] < df['BBU_30_1.618'].iloc[-1] and df.Close.iloc[-1] > df['BBM_30_1.382'].iloc[-1] and
        df.Close.iloc[-1] < df.Open.iloc[-1] and
        df.Close.iloc[-2] > df.Open.iloc[-2] and
        df.Open.iloc[-1] > df.Close.iloc[-2] and
        df.Close.iloc[-1] < df.Open.iloc[-2] ):
            return 1
        
        #nosignal
        else:
            return 0

    def bollinger_engulfing_total_signal(self, df):
        signal = [0]*len(df)
        for i in range(20, len(df)):
            dfpl = df.iloc[i-4:i]
            signal[i]= self.bollinger_engulfing_signal_func(dfpl)
        df["bollinger_engulfing_signal"] = signal
        return df
    
    def totalSignal_2(self, df):
        ordersignal = [0] * len(df)
        for i in range(0, len(df)):
            if df["bollinger_engulfing_signal"].iloc[i] == 2:
                ordersignal[i] = 2
            elif df["bollinger_engulfing_signal"].iloc[i] == 1:
                ordersignal[i] = 1
        df.loc[:, 'ordersignal'] = ordersignal
        ordersignal_buy_count = sum(1 for x in df['ordersignal'] if x == 2)
        ordersignal_sell_count = sum(1 for x in df['ordersignal'] if x == 1)

        print(f"len_df: {len(df)}")
        print(f"ordersignal_buy_count: {ordersignal_buy_count}")
        print(f"ordersignal_sell_count: {ordersignal_sell_count}")
        return df
    
    def init_bb_doji_eng_pattern(self, data):
        data = self.bb_calculator(data)
        data = self.bollinger_engulfing_total_signal(data)        
        data = self.totalSignal_2(data)
        data.dropna(inplace=True)
        return data


