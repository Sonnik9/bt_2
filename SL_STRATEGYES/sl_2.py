from IND_STRATEGIES.ind_1 import HEIKEN_ASHI_STRATEGY
import talib
import pandas_ta as ta
from finta import TA
import math

class SL_STRATEGY_TWOO(HEIKEN_ASHI_STRATEGY):

    def __init__(self) -> None:
        super().__init__()
        
    def calculate_pandas_atr(self, data, period=14):        
        # data.sort_index(ascending=True, inplace=True)       
        atr_data = ta.atr(data['High'], data['Low'], data['Close'], timeperiod=period)                          
        atr_data = atr_data.dropna()
        last_atr = atr_data.iloc[-1]        
        return last_atr
    
    def calculate_talib_atr(self, data, period=14):
        atr = None
        try:
            atr = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=period)
            atr = atr.to_numpy()[-1]
        except Exception as ex:
            print(f"Error in calculate_atr: {ex}")
        return atr

    def sl_tp_calculations(self, data, direction):
        # piv_info_repl = self.calculate_manualy_pivot(data)
        # piv_info_repl = self.calculate_finta_pivot(data)        
        # resistance_piv, support_piv = piv_info_repl[f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}'], piv_info_repl[f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}']
        # ////////////////////////////////////////////////////////////
        atr1 = self.calculate_pandas_atr(data)
        atr2 = self.calculate_talib_atr(data)
        atr = (abs(atr1) + abs(atr2)) / 2
        l_pr = data['Close'].iloc[-1]
        if direction == 2:
            tp, sl = l_pr + atr*1.2, l_pr - atr*0.9
            # print(f"sl_L_level: {sl}, close_price: {l_pr}, tp_L_level: {tp}")
            if sl >= tp or tp <= l_pr or sl >= l_pr:
                raise ValueError("For a long order, SL should be less than TP.")         

        elif direction == 1:
            sl, tp = l_pr + atr*0.9, l_pr - atr*1.2
            # print(f"sl_S_level: {sl}, close_price: {l_pr}, tp_S_level: {tp}")
            if sl <= tp or tp >= l_pr or sl <= l_pr:
                raise ValueError("For a long order, SL should be less than TP.")  
        
        return sl, tp

    def sl_generator_two(self, data):
        SL_Signal = [0] * len(data)
        TP_Signal = [0] * len(data)
        SLbackcandles = 30

        for row in range(SLbackcandles, len(data)):
            defender = data['ordersignal'].iloc[row]
            if data['ordersignal'].iloc[row] == 2 or data['ordersignal'].iloc[row] == 1:                
                sl, tp = self.sl_tp_calculations(data.iloc[:row], defender)
                SL_Signal[row] = sl
                TP_Signal[row] = tp
                
        data.loc[:, 'SLSignal'] = SL_Signal
        data.loc[:, 'TPSignal'] = TP_Signal
        # data.loc[:, 'SL_S_Signal'] = SL_S_Signal
        # data.loc[:, 'TP_S_Signal'] = TP_S_Signal
        # print(data.loc[:, 'TPSignal'].to_list())
        return data





# ghf = SL_STRATEGY_TWO()

# python -m SL_STRATEGYES.sl_2
