import yfinance as yf
import pandas as pd

class GETT_HISTORICAL_DATA():

    def __init__(self) -> None:
        pass

    def get_historical_data(self, symbol):
        ticker = yf.Ticker(symbol)
        data = ticker.history(start='2012-03-11', end='2022-07-10')
        data.drop(['Dividends'], axis=1, inplace=True)
        data.drop(['Stock Splits'], axis=1, inplace=True)        
        data.reset_index(inplace=True)        
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
          
        # data.drop(['Date'], axis=1, inplace=True)
        # data.rename(columns={'Date': 'Time'}, inplace=True)   
        # data.set_index('Time', inplace=True)     
        # data.head(10)
        return data