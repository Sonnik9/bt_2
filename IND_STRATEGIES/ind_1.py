import pandas_ta as ta
from pparamss import INIT_PARAMS

class HEIKEN_ASHI_PATTERN(INIT_PARAMS):
    def __init__(self) -> None: 
        super().__init__()       
        # self.dfpl = None

    def HeikenPreparators(self, data):  
        
        data['Heiken_Close'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
        data['Heiken_Open'] = data['Open']
        for i in range(1, len(data)):
            data.loc[i, 'Heiken_Open'] = (data['Heiken_Open'].iloc[i-1] + data['Heiken_Close'].iloc[i-1]) / 2
        data['Heiken_High'] = data[['High', 'Heiken_Open', 'Heiken_Close']].max(axis=1)
        data['Heiken_Low'] = data[['Low', 'Heiken_Open', 'Heiken_Close']].min(axis=1)
        data.dropna(inplace=True)
        
        data["EMA10"] = ta.ema(data['Close'], length=10)
        data["EMA30"] = ta.ema(data['Close'], length=30)
        # data['RSI'] = ta.rsi(data['Close'], length=12)
        data.dropna(inplace=True)
        return data

    def HeikenSignal1(self, dff):
        df = dff.copy()
        signal1 = [0] * len(df)
        ratio = 0.7
        
        for i in range(1, len(df)):
            PreviousHeikenBody = abs(df['Heiken_Open'].iloc[i-1] - df['Heiken_Close'].iloc[i-1])

            if PreviousHeikenBody != 0:
                condition_up = (
                    (df['Heiken_High'].iloc[i-1] - max(df['Heiken_Open'].iloc[i-1], df['Heiken_Close'].iloc[i-1])) /
                    PreviousHeikenBody > ratio and
                    (min(df['Heiken_Open'].iloc[i-1], df['Heiken_Close'].iloc[i-1]) - df['Heiken_Low'].iloc[i-1]) /
                    PreviousHeikenBody > ratio and
                    (df['Heiken_Open'].iloc[i] < df['Heiken_Close'].iloc[i] and
                    df['Heiken_Low'].iloc[i] >= df['Heiken_Open'].iloc[i])
                )

                condition_down = (
                    (df['Heiken_High'].iloc[i-1] - max(df['Heiken_Open'].iloc[i-1], df['Heiken_Close'].iloc[i-1])) /
                    PreviousHeikenBody > ratio and
                    (min(df['Heiken_Open'].iloc[i-1], df['Heiken_Close'].iloc[i-1]) - df['Heiken_Low'].iloc[i-1]) /
                    PreviousHeikenBody > ratio and
                    (df['Heiken_Open'].iloc[i] > df['Heiken_Close'].iloc[i] and
                    df['Heiken_High'].iloc[i] <= df['Heiken_Open'].iloc[i])
                )

                if condition_up:                    
                    signal1[i] = 2
                    # df.loc[i, 'HeikenSignal1'] = 2
                elif condition_down:                    
                    signal1[i] = 1
                    # df.loc[i, 'HeikenSignal1'] = 1
                else:
                    signal1[i] = 0
                    # df.loc[i, 'HeikenSignal1'] = 0

        # df['HeikenSignal1'] = signal1
        df.loc[:, 'HeikenSignal1'] = signal1
        # df_new = df.copy()
        # df_new.dropna(inplace=True)

        return df


    def totalSignal_1(self, dff):
        df = dff.copy()
        ordersignal = [0] * len(df)
        # df.loc[:, 'ordersignal'] = ordersignal        

        for i in range(0, len(df)):
            if (
                df['EMA10'].iloc[i] > df['EMA30'].iloc[i] and
                df['Heiken_Open'].iloc[i] < df['EMA10'].iloc[i] and
                df['Heiken_Close'].iloc[i] > df['EMA10'].iloc[i] and
                df['HeikenSignal1'].iloc[i] == 2
            ):
                ordersignal[i] = 2
                # df.loc[i, 'ordersignal'] = 2

            elif (
                df['EMA10'].iloc[i] < df['EMA30'].iloc[i] and
                df['Heiken_Open'].iloc[i] > df['EMA10'].iloc[i] and
                df['Heiken_Close'].iloc[i] < df['EMA10'].iloc[i] and
                df['HeikenSignal1'].iloc[i] == 1
            ):
                ordersignal[i] = 1
                # df.loc[i, 'ordersignal'] = 1

            else:
                # df['ordersignal'].iloc[i] = 0
                pass
        
        df.loc[:, 'ordersignal'] = ordersignal
        # df['ordersignal'] = ordersignal
        # df.dropna(inplace=True)
        ordersignal_buy_count = sum(1 for x in df['ordersignal'] if x == 2)
        ordersignal_sell_count = sum(1 for x in df['ordersignal'] if x == 1)

        print(f"len_df: {len(df)}")
        print(f"ordersignal_buy_count: {ordersignal_buy_count}")
        print(f"ordersignal_sell_count: {ordersignal_sell_count}")
        return df
    
    def init_heiken_pattern(self, data):
        data = self.HeikenPreparators(data)
        # print(data)
        data = data[data.Open != data.Close]
        data = self.HeikenSignal1(data)
        data = self.totalSignal_1(data)
        print(data)
        data.dropna(inplace=True)

        return data




