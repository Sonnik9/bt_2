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
        data['RSI'] = ta.rsi(data['Close'], length=12)
        data.dropna(inplace=True)
        return data

    def HeikenSignal1(self, df):
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
                elif condition_down:                    
                    signal1[i] = 1

        df['HeikenSignal1'] = signal1

        return df


    def totalSignal(self, df):
        ordersignal = [0] * len(df)

        for i in range(0, len(df)):
            if (
                df['EMA10'].iloc[i] > df['EMA30'].iloc[i] and
                df['Heiken_Open'].iloc[i] < df['EMA10'].iloc[i] and
                df['Heiken_Close'].iloc[i] > df['EMA10'].iloc[i] and
                df['HeikenSignal1'].iloc[i] == 2
            ):
                ordersignal[i] = 2

            if (
                df['EMA10'].iloc[i] < df['EMA30'].iloc[i] and
                df['Heiken_Open'].iloc[i] > df['EMA10'].iloc[i] and
                df['Heiken_Close'].iloc[i] < df['EMA10'].iloc[i] and
                df['HeikenSignal1'].iloc[i] == 1
            ):
                ordersignal[i] = 1

        df.loc[:, 'ordersignal'] = ordersignal
        ordersignal_buy_count = sum(1 for x in df['ordersignal'] if x == 2)
        ordersignal_sell_count = sum(1 for x in df['ordersignal'] if x == 1)

        print(f"len_df: {len(df)}")
        print(f"ordersignal_buy_count: {ordersignal_buy_count}")
        print(f"ordersignal_sell_count: {ordersignal_sell_count}")
        return df


