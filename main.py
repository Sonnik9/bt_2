import math
import pandas_ta as ta
import numpy as np
import yfinance as yf
import pandas as pd
from backtesting import Strategy, Backtest

class GETT_HISTORICAL_DATA():
    def __init__(self) -> None:
        pass
                
    def get_historical_data(self, symbol):           
        data = yf.download(tickers=symbol, start='2018-03-11', end='2022-07-10')
        data.drop(['Volume'], axis=1, inplace=True)
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)  # Ensure 'Date' column is set as the index
        data.sort_index(inplace=True)  # Make sure the data is sorted by date
        return data

class CALCULATIONS(GETT_HISTORICAL_DATA):
    def __init__(self) -> None:
        self.dfpl = None

    def HeikenPreparators(self, data):  
        
        data['Heiken_Close'] = (data['Open'] + data['Close'] + data['High'] + data['Low']) / 4
        data['Heiken_Open'] = data['Open']
        for i in range(1, len(data)):
            data.loc[i, 'Heiken_Open'] = (data['Heiken_Open'].iloc[i-1] + data['Heiken_Close'].iloc[i-1]) / 2
        data['Heiken_High'] = data[['High', 'Heiken_Open', 'Heiken_Close']].max(axis=1)
        data['Heiken_Low'] = data[['Low', 'Heiken_Open', 'Heiken_Close']].min(axis=1)
        data.dropna(inplace=True)
        data.head(10)

        data["EMA10"] = ta.ema(data['Close'], length=10)
        data["EMA30"] = ta.ema(data['Close'], length=30)
        data['RSI'] = ta.rsi(data['Close'], length=12)
        data.dropna(inplace=True)
        return data

    def HeikenSignal1(self, df):
        # signal1 = [0] * len(df)
        ratio = 1.5
        ordersignal = [0] * len(df)

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
                    ordersignal[i] = 2
                    # signal1[i] = 2
                elif condition_down:
                    ordersignal[i] = 1
                    # signal1[i] = 1
        df.loc[:, 'ordersignal'] = ordersignal
        # df['ordersignal'] = signal1
        ordersignal_buy_count = sum(1 for x in df['ordersignal'] if x == 2)
        ordersignal_sell_count = sum(1 for x in df['ordersignal'] if x == 1)
        # df['HeikenSignal1'] = signal1
        # ordersignal_buy_count = sum(1 for x in df['HeikenSignal1'] if x == 2)
        # ordersignal_sell_count = sum(1 for x in df['HeikenSignal1'] if x == 1)

        print(f"len_df: {len(df)}")
        print(f"heiken_buy_count: {ordersignal_buy_count}")
        print(f"heiken_sell_count: {ordersignal_sell_count}")

        return df


    # def totalSignal(self, df):
    #     ordersignal = [0] * len(df)

    #     for i in range(0, len(df)):
    #         if (
    #             df['EMA10'].iloc[i] > df['EMA30'].iloc[i] and
    #             df['Heiken_Open'].iloc[i] < df['EMA10'].iloc[i] and
    #             df['Heiken_Close'].iloc[i] > df['EMA10'].iloc[i] and
    #             df['HeikenSignal1'].iloc[i] == 2
    #         ):
    #             ordersignal[i] = 2

    #         if (
    #             df['EMA10'].iloc[i] < df['EMA30'].iloc[i] and
    #             df['Heiken_Open'].iloc[i] > df['EMA10'].iloc[i] and
    #             df['Heiken_Close'].iloc[i] < df['EMA10'].iloc[i] and
    #             df['HeikenSignal1'].iloc[i] == 1
    #         ):
    #             ordersignal[i] = 1

    #     df.loc[:, 'ordersignal'] = ordersignal
    #     ordersignal_buy_count = sum(1 for x in df['ordersignal'] if x == 2)
    #     ordersignal_sell_count = sum(1 for x in df['ordersignal'] if x == 1)

    #     print(f"len_df: {len(df)}")
    #     print(f"ordersignal_buy_count: {ordersignal_buy_count}")
    #     print(f"ordersignal_sell_count: {ordersignal_sell_count}")
    #     return df
    
    def pointpos(self, x):
        if x['ordersignal'] == 1:
            return x['High'] + 1e-4
        elif x['ordersignal'] == 2:
            return x['Low'] - 1e-4
        else:
            return np.nan

    def sl_generator(self, data):
        SLSignal = [0] * len(data)
        SLbackcandles = 1

        for row in range(SLbackcandles, len(data)):
            mi = 1e10
            ma = -1e10
            if data['ordersignal'].iloc[row] == 1:
                for i in range(row - SLbackcandles, row + 1):
                    ma = max(ma, data['High'].iloc[i])
                SLSignal[row] = ma

            if data['ordersignal'].iloc[row] == 2:
                for i in range(row - SLbackcandles, row + 1):
                    mi = min(mi, data['Low'].iloc[i])
                SLSignal[row] = mi

        data.loc[:, 'SLSignal'] = SLSignal
        self.dfpl = data

    # def SIGNAL(self):        
    #     return self.dfpl['ordersignal']

class MAIN_INIT(CALCULATIONS):
    def __init__(self) -> None:
        super().__init__()

    def go_(self, symbol, slicee):
        data = self.get_historical_data(symbol)
        data = self.HeikenPreparators(data)
        data = data[data.Open != data.Close]
        data = data.reset_index()
        data = self.HeikenSignal1(data)
        # data = self.totalSignal(data)
        data.dropna(inplace=True)
        data.reset_index(inplace=True)
        data['pointpos'] = data.apply(lambda row: self.pointpos(row), axis=1)
        self.sl_generator(data)
        self.dfpl = self.dfpl[slicee:]

    def SIGNAL(self):        
        return self.dfpl['ordersignal']

# import numpy as np
# import pandas as pd

def main(symbol, slicee):
    mainn_init = MAIN_INIT()
    mainn_init.go_(symbol, slicee)
    # mainn_init.dfpl.index = pd.RangeIndex(len(mainn_init.dfpl))
    # mainn_init.dfpl.index = pd.to_datetime(mainn_init.dfpl.index)

    class MyCandlesStrat(Strategy):
        sltr = 20
        mysize = 0.005

        def init(self):
            super().init()
            # print(f"Type of mainn_init.SIGNAL: {type(mainn_init.SIGNAL)}")
            # print(f"Values in mainn_init.SIGNAL: {mainn_init.SIGNAL}")
            # self.signal1 = self.I(mainn_init.SIGNAL)
            self.signal1 = self.I(mainn_init.SIGNAL)

        def next(self):
            super().next()
            self.sltr = 1.5
            self.mysize = 0.005

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

    # Convert the index to a simple period index
    mainn_init.dfpl.index = pd.RangeIndex(len(mainn_init.dfpl))

    bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=10000, margin=1/50, commission=.001)
    stat = bt.run()
    print(stat)

if __name__ == "__main__":
    symbol = '^RUI'
    slicee = 10
    main(symbol, slicee)
