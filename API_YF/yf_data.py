import yfinance as yf
import pandas as pd

class GETT_HISTORICAL_DATA():

    def __init__(self) -> None:
        pass

    def get_historical_data(self, symbol):
        start= "2022-01-1"
        end="2023-11-19"
        # start = "2021-12-1"
        # end = "2023-3-19"
        # ticker = yf.Ticker(symbol)
        # data = ticker.history(start=start, end=end)
        data = yf.download(symbol, start=start, end=end, interval='1h')
        # print(data)
        try:
            data.drop(['Dividends'], axis=1, inplace=True)
            data.drop(['Stock Splits'], axis=1, inplace=True)     
        except:
            pass   
        data.reset_index(inplace=True)   
        try:
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')   
        except:
            pass  
        try:
            data['Date'] = data['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
          
        # data.drop(['Date'], axis=1, inplace=True)
        # data.rename(columns={'Date': 'Time'}, inplace=True)   
        # data.set_index('Time', inplace=True)     
        # data.head(10)
        return data