from config import Configg
import pandas as pd

class GETT_API(Configg):
    
    def __init__(self) -> None:
        super().__init__()  
        self.end_date = 3
        

    def get_all_tickers(self):
        method = 'GET'

        all_tickers = None
        url = self.URL_PATTERN_DICT['all_tikers_url']       
        # print(url)
        all_tickers = self.HTTP_request(url, method=method, headers=self.header)

        return all_tickers
    
    def get_excangeInfo(self, symbol):
        method = 'GET'

        exchangeInfo = None
        if symbol:            
            url = f"{self.URL_PATTERN_DICT['exchangeInfo_url']}?symbol={symbol}"
        else:
            url = self.URL_PATTERN_DICT['exchangeInfo_url']        
        exchangeInfo = self.HTTP_request(url, method=method, headers=self.header)

        return exchangeInfo
    
    def get_balance(self):
        method = 'GET'

        current_balance = None  
         
        locked_balance = None  
        un_pNl_balance = None   
        url = self.URL_PATTERN_DICT['balance_url']
        params = {}
        params['recvWindow'] = 5000
        params = self.get_signature(params)
        current_balance = self.HTTP_request(url, method=method, headers=self.header, params=params)
        # print(current_balance)
        if self.market == 'spot':
            # print('hi spot')
            current_balance = dict(current_balance)
            # print(current_balance)
            current_balanceE = current_balance['balances']
            current_balance = [(x['free'], x['locked']) for x in current_balanceE if x['asset'] == 'USDT'][0]          
        if self.market == 'futures':
            # print('hi futures')
            current_balanceE = list(current_balance)
            current_balance = [(x['balance'], x['crossUnPnl']) for x in current_balanceE if x['asset'] == 'USDT'][0]
        return current_balance
    
    def get_position_price(self, symbol):
        method = 'GET'

        positions = None        
        url = self.URL_PATTERN_DICT['positions_url']
        params = {}
        params = self.get_signature(params)
        positions = self.HTTP_request(url, method=method, headers=self.header, params=params)
        # print(positions)
        positions = float([x for x in positions if x['symbol'] == symbol][0]["entryPrice"])

        return positions
    
    def get_klines(self, symbol, end_date=Configg().end_date):
        method = 'GET'
        klines = None
        data = None
        url = self.URL_PATTERN_DICT["klines_url"]
        # print(url)

        params = {}
        params["symbol"] = symbol
        params["interval"] = self.INTERVAL

        if end_date:            
           params["endTime"] = int(end_date.timestamp() * 1000)
        params["limit"] = self.KLINES_PERIOD + 1
        # params = self.get_signature(params)
        # print(params)
        klines = self.HTTP_request(url, method=method, headers=self.header, params=params)
        # print(klines)
        if klines:
            try:
                data = pd.DataFrame(klines).iloc[:, :6]
                data.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
                data = data.set_index('Time')
                data.index = pd.to_datetime(data.index, unit='ms')
                data = data.astype(float)
            except:
                pass
        
        return data
    
# ////////////////////////////////////////////////////////////////////////////////////

    def get_all_orders(self):
        method = 'GET'

        all_orders = None        
        params = {}               
        url = self.URL_PATTERN_DICT['get_all_orders_url']
        params = self.get_signature(params)
        all_orders = self.HTTP_request(url, method=method, headers=self.header, params=params)

        return all_orders
    
    def get_open_positions(self):
        method = 'GET'

        all_positions = None        
        params = {}          
        symbol = None     
        url = self.URL_PATTERN_DICT['positions_url']
        if symbol:
            params["symbol"] = symbol
        params = self.get_signature(params)
        all_positions = self.HTTP_request(url, method=method, headers=self.header, params=params)
        all_positions = [x for x in all_positions if float(x["positionAmt"]) != 0]

        return all_positions 
# //////////////////////////////////////////////////////////////////////////////////

# get_apii = GETT_API()

# kl = get_apii.get_klines('BNBUSDT')
# print(kl)
# python -m API_BINANCE.get_api
