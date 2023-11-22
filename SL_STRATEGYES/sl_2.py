from IND_STRATEGIES.ind_strategy_1 import HEIKEN_ASHI_STRATEGY
import talib
import pandas_ta as ta
from finta import TA
import math

class SL_STRATEGY_TWOO(HEIKEN_ASHI_STRATEGY):

    def __init__(self) -> None:
        super().__init__()
        # print(self.PIVOT_GENERAL_TYPE)

    def calculate_pandas_atr(self, data, period=14):        
        data.sort_index(ascending=True, inplace=True)       
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
    
    def determine_pivot_type(self, atr_list, last_atr):
        pivot_type = None
        sorted_atr = sorted(atr_list)
        len_sorted_atr = len(sorted_atr)
        sort_grade = len_sorted_atr/5
        atr_index = [i for i, item in enumerate(sorted_atr) if float(item) == float(last_atr)][0]
        pivot_type = atr_index / sort_grade    
        pivot_type = math.ceil((pivot_type * 10) / 10)
        if pivot_type > 5: pivot_type = 5
        if pivot_type < 1: pivot_type = 1
        return pivot_type
    
    def calculate_fibonacci_pivot_points(self, data):
        data = data.iloc[-30:] 
        latest_pivot_dict = {}
        piv_repl = {}
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            pivot = (high + low + close) / 3
            # support1 = pivot - 0.382 * (high - low)
            # support2 = pivot - 0.618 * (high - low)
            # support3 = pivot - (high - low)
            # support3 = pivot - 1.382 * (high - low) 
            support1 = pivot - 1.618 * (high - low)
            support2 = pivot - 2.618 * (high - low)  
            support3 = pivot - 4.236 * (high - low)
            support4 = pivot - 6.854 * (high - low)
            support5 = pivot - 11.090 * (high - low)  
            # resistance1 = pivot + 0.382 * (high - low)
            # resistance2 = pivot + 0.618 * (high - low)
            # resistance3 = pivot + (high - low)
            # resistance4 = pivot + 1.382 * (high - low) 
            resistance1 = pivot + 1.618 * (high - low) 
            resistance2 = pivot + 2.618 * (high - low)
            resistance3 = pivot + 4.236 * (high - low)  
            resistance4 = pivot + 6.854 * (high - low)
            resistance5 = pivot + 11.090 * (high - low)          
            
            latest_pivot_dict = {
                'pp': pivot.iloc[-1],
                'S1': support1.iloc[-1],
                'S2': support2.iloc[-1],
                'S3': support3.iloc[-1],
                'S4': support4.iloc[-1], 
                'S5': support5.iloc[-1],  
                # 'S6': support6.iloc[-1],
                # 'S7': support7.iloc[-1],
                'R1': resistance1.iloc[-1],
                'R2': resistance2.iloc[-1],
                'R3': resistance3.iloc[-1],
                'R4': resistance4.iloc[-1], 
                'R5': resistance5.iloc[-1],
                # 'R6': resistance6.iloc[-1],
                # 'R7': resistance7.iloc[-1]   
            }
            # self.pivot_levels_type = 6  # Update the number of pivot levels
            piv_repl = {
                f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
                f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
            }
        except Exception as ex:
            print(ex)

        return piv_repl

    def calculate_classic_pivot_points(self, data):
        data = data.iloc[-30:]
        latest_pivot_dict = {}
        piv_repl = {} 
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']

            pivot = (high + low + close) / 3
            # support1 = (2 * pivot) - high
            # support2 = pivot - (high - low)
            # support2 = pivot - 2 * (high - low)
            support1 = pivot - 3 * (high - low)
            support2 = pivot - 4 * (high - low)  
            support3 = pivot - 5 * (high - low)
            support4 = pivot - 6 * (high - low)
            support5 = pivot - 7 * (high - low)  
            # resistance1 = (2 * pivot) - low
            # resistance2 = pivot + (high - low)
            # resistance3 = pivot + 2 * (high - low)
            # resistance4 = pivot + 3 * (high - low)  
            resistance1 = pivot + 3 * (high - low)
            resistance2 = pivot + 4 * (high - low)
            resistance3 = pivot + 5 * (high - low)
            resistance4 = pivot + 6 * (high - low)
            resistance5 = pivot + 7 * (high - low)  
            
            latest_pivot_dict = {
                'pp': pivot.iloc[-1],
                'S1': support1.iloc[-1],
                'S2': support2.iloc[-1],
                'S3': support3.iloc[-1],
                'S4': support4.iloc[-1], 
                'S5': support5.iloc[-1],  
                # 'S6': support6.iloc[-1],
                # 'S7': support7.iloc[-1],
                'R1': resistance1.iloc[-1],
                'R2': resistance2.iloc[-1],
                'R3': resistance3.iloc[-1],
                'R4': resistance4.iloc[-1], 
                'R5': resistance5.iloc[-1],
                # 'R6': resistance6.iloc[-1],
                # 'R7': resistance7.iloc[-1]   
            }
            # self.pivot_levels_type = 4  # Update the number of pivot levels
            piv_repl = {
                f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
                f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
            }
        except Exception as ex:
            print(f"str31: {ex}")

        return piv_repl

    def calculate_manualy_pivot(self, data):
        piv = None
        if self.PIVOT_GENERAL_TYPE == 'Classic':
            piv = self.calculate_classic_pivot_points(data)
        elif self.PIVOT_GENERAL_TYPE == 'Fibonacci':
            piv = self.calculate_fibonacci_pivot_points(data)

        return piv

    def calculate_finta_pivot(self, dataa, period=30):
        # finta
        # dataa = data.copy()
        piv_repl = {}
        piv = None
   
        if self.PIVOT_GENERAL_TYPE == 'Classic':
            piv = TA.PIVOT(dataa)
        elif self.PIVOT_GENERAL_TYPE == 'Fibonacci':
            piv = TA.PIVOT_FIB(dataa)

        latest_pivot = piv.iloc[-period:]
        pivot_mean = latest_pivot.mean()
        latest_pivot_dict = {
            'pp': pivot_mean['pivot'],
            'S1': pivot_mean['s1'],
            'S2': pivot_mean['s2'],
            'S3': pivot_mean['s3'],
            'S4': pivot_mean['s4'],
         
            'R1': pivot_mean['r1'],
            'R2': pivot_mean['r2'],
            'R3': pivot_mean['r3'],
            'R4': pivot_mean['r4']            
        }
        # self.pivot_levels_type = 4
        piv_repl = {
            f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
            f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
        }

        return piv_repl
    
    def pv_sl_tp_calculations(self, data, direction):
        # piv_info_repl = self.calculate_manualy_pivot(data)
        # piv_info_repl = self.calculate_finta_pivot(data)        
        # resistance_piv, support_piv = piv_info_repl[f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}'], piv_info_repl[f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}']
        # ////////////////////////////////////////////////////////////
        atr = self.calculate_pandas_atr(data)
        atr = abs(atr)
        l_pr = data['Close'].iloc[-1]
        if direction == 2:
            tp, sl = l_pr + atr*1.2, l_pr - atr*0.9
            # print(f"sl_L_level: {sl}, close_price: {l_pr}, tp_L_level: {tp}")
            if sl >= tp:
                raise ValueError("For a long order, SL should be less than TP.")         

        elif direction == 1:
            sl, tp = l_pr + atr*0.9, l_pr - atr*1.2
            # print(f"sl_S_level: {sl}, close_price: {l_pr}, tp_S_level: {tp}")
            if sl <= tp:
                raise ValueError("For a long order, SL should be less than TP.")  
        
        return sl, tp

    def sl_generator_two(self, data):
        SL_L_Signal = [0] * len(data)
        TP_L_Signal = [0] * len(data)
        SL_S_Signal = [0] * len(data)
        TP_S_Signal = [0] * len(data)
        SLbackcandles = 30

        for row in range(SLbackcandles, len(data)):

            defender = data['ordersignal'].iloc[row]
            if data['ordersignal'].iloc[row] == 2:                
                sl, tp = self.pv_sl_tp_calculations(data.iloc[:row], defender)
                SL_L_Signal[row] = sl
                TP_L_Signal[row] = tp
            elif data['ordersignal'].iloc[row] == 1:
                sl, tp = self.pv_sl_tp_calculations(data.iloc[:row], defender)
                SL_S_Signal[row] = sl
                TP_S_Signal[row] = tp
                
        data.loc[:, 'SL_L_Signal'] = SL_L_Signal
        data.loc[:, 'TP_L_Signal'] = TP_L_Signal
        data.loc[:, 'SL_S_Signal'] = SL_S_Signal
        data.loc[:, 'TP_S_Signal'] = TP_S_Signal
        # print(data.loc[:, 'TPSignal'].to_list())
        self.dfpl = data





# ghf = SL_STRATEGY_TWO()

# python -m SL_STRATEGYES.sl_2