from datetime import datetime

class BASIC_PARAMETRS():
    def __init__(self):
        # super().__init__()
        self.SOLI_DEO_GLORIA = 'Soli Deo Gloria!'        
        self.market = 'futures'
        self.test_flag = False # -- real    
        # self.market = 'futures'
        # self.test_flag = True # -- test            

class URL_TEMPLATES(BASIC_PARAMETRS):
    def __init__(self) -> None:
        super().__init__()        
        self.URL_PATTERN_DICT= {}              

    def init_urls(self):        
        if self.market == 'spot':                
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://api.binance.com/api/v3/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://api.binance.com/api/v3/order' 
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://api.binance.com/api/v3/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://api.binance.com/api/v3/account'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://api.binance.com/api/v3/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://api.binance.com/api/v3/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://api.binance.com/api/v3/account'
            # print('hi')
            self.URL_PATTERN_DICT["klines_url"] = 'https://api.binance.com/api/v3/klines'

        else:
            self.URL_PATTERN_DICT['all_tikers_url'] = "https://fapi.binance.com/fapi/v1/ticker/24hr"
            self.URL_PATTERN_DICT['create_order_url'] = 'https://fapi.binance.com/fapi/v1/order' 
            self.URL_PATTERN_DICT['exchangeInfo_url'] = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
            self.URL_PATTERN_DICT['balance_url'] = 'https://fapi.binance.com/fapi/v2/balance'
            self.URL_PATTERN_DICT['get_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/openOrders'
            self.URL_PATTERN_DICT['cancel_all_orders_url'] = 'https://fapi.binance.com/fapi/v1/allOpenOrders'
            self.URL_PATTERN_DICT['positions_url'] = 'https://fapi.binance.com/fapi/v2/positionRisk'
            self.URL_PATTERN_DICT["set_leverage_url"] = 'https://fapi.binance.com/fapi/v1/leverage'
            self.URL_PATTERN_DICT["klines_url"] = 'https://fapi.binance.com/fapi/v1/klines'

class TIME_TEMPLATES(URL_TEMPLATES):   
    def __init__(self) -> None:
        super().__init__()
        self.KLINE_TIME, self.TIME_FRAME = 1, 'h'
        self.INTERVAL = str(self.KLINE_TIME) + self.TIME_FRAME
        self.KLINES_PERIOD = 160   
        self.end_date = None      

class INDICATORD_PARAMS(TIME_TEMPLATES):
    def __init__(self) -> None:
        super().__init__()
        self.b_bband_q, self.s_bband_q = 1, 1
        self.b_rsi_lev, self.s_rsi_lev = 37, 63 
        self.b_rsi_diver_lev = 50 
        self.rsi_period = 14   
        self.b_macd_q, self.s_macd_q = 1, 1
        self.b_stoch_q, self.s_stoch_q = 23, 77

class FILTER_SET(INDICATORD_PARAMS):
    def __init__(self) -> None:
        super().__init__()
        self.SLICE_VOLUME_PAIRS = 41 # volums
        self.SLICE_VOLATILITY = 39 # volatility
        self.MIN_FILTER_PRICE = 0.01 # min price
        self.MAX_FILTER_PRICE = 3000000 # max price
        # self.problem_pairs = ['SOLUSDT', 'ZECUSDT', 'MKRUSDT', 'COMPUSDT', 'ORDIUSDT']
        self.problem_pairs = ['DOGEUSDT'] # problem coins list

class STRATEGY_SET(FILTER_SET):
    def __init__(self) -> None:
        super().__init__()  
        self.BUNCH_DICT = {}      
        self.T_BUNCH_VARIANT = 1
        self.F_BUNCH_VARIANT = 1      
        # self.PIVOT_GENERAL_TYPE = 'Classic'
        self.PIVOT_GENERAL_TYPE = 'Fibonacci'
        self.pivot_levels_type = 5
        self.kline_period_for_piv = 30
        self.grid_decimal = 5       

    def update_strategy_set(self, new_T_bunch_variant, new_F_bunch_variant):
        self.T_BUNCH_VARIANT = new_T_bunch_variant
        self.F_BUNCH_VARIANT = new_F_bunch_variant

    def init_strategy_set(self):
        self.BUNCH_DICT['T'] = [
            self.SOLI_DEO_GLORIA,     
            ['rsi_diver_pattern_flag', 'ma_crossover_strong_flag'],      
            ['bband_flag', 'macd_lite_flag', 'ma_crossover_strong_flag'], 
            
            ['bband_flag', 'heikin_ashi_flag'],    
            ['bband_flag', 'macd_lite_flag'],                   
            ['bband_flag', 'rsi_overtrading_flag'], 
            # ['bband_flag', 'macd_strong_flag'],
            # ['bband_flag', 'macd_lite_flag', 'ma_crossover_lite_flag'],          
            # ['ma_crossover_strong_flag'],
            # ['ma_crossover_lite_flag']            
        ]
        self.BUNCH_DICT['F'] = [
            self.SOLI_DEO_GLORIA,
            ['rsi_diver_pattern_flag', 'ma_crossover_lite_flag'],
            ['bband_flag', 'rsi_diver_pattern_flag'], 
            # ['bband_flag', 'macd_lite_flag'],                     
            # ['bband_flag', 'rsi_overtrading_flag'],
            ['macd_lite_flag', 'ma_crossover_lite_flag'],
            
            # ['stoch_flag'],
            # ['ma_crossover_strong_flag'],
            # ['ma_crossover_lite_flag'],
            
        ]

class INIT_PARAMS(STRATEGY_SET):
    def __init__(self) -> None:
        super().__init__()
        self.init_itits()

    def init_itits(self):
        self.init_urls()
        self.init_strategy_set()



# python -m pparamss
