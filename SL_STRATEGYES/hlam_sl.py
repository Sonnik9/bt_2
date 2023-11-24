


    # def determine_pivot_type(self, atr_list, last_atr):
    #     pivot_type = None
    #     sorted_atr = sorted(atr_list)
    #     len_sorted_atr = len(sorted_atr)
    #     sort_grade = len_sorted_atr/5
    #     atr_index = [i for i, item in enumerate(sorted_atr) if float(item) == float(last_atr)][0]
    #     pivot_type = atr_index / sort_grade    
    #     pivot_type = math.ceil((pivot_type * 10) / 10)
    #     if pivot_type > 5: pivot_type = 5
    #     if pivot_type < 1: pivot_type = 1
    #     return pivot_type
    
    # def calculate_fibonacci_pivot_points(self, data):
    #     data = data.iloc[-30:] 
    #     latest_pivot_dict = {}
    #     piv_repl = {}
    #     try:
    #         high = data['High']
    #         low = data['Low']
    #         close = data['Close']
            
    #         pivot = (high + low + close) / 3
    #         # support1 = pivot - 0.382 * (high - low)
    #         # support2 = pivot - 0.618 * (high - low)
    #         # support3 = pivot - (high - low)
    #         # support3 = pivot - 1.382 * (high - low) 
    #         support1 = pivot - 1.618 * (high - low)
    #         support2 = pivot - 2.618 * (high - low)  
    #         support3 = pivot - 4.236 * (high - low)
    #         support4 = pivot - 6.854 * (high - low)
    #         support5 = pivot - 11.090 * (high - low)  
    #         # resistance1 = pivot + 0.382 * (high - low)
    #         # resistance2 = pivot + 0.618 * (high - low)
    #         # resistance3 = pivot + (high - low)
    #         # resistance4 = pivot + 1.382 * (high - low) 
    #         resistance1 = pivot + 1.618 * (high - low) 
    #         resistance2 = pivot + 2.618 * (high - low)
    #         resistance3 = pivot + 4.236 * (high - low)  
    #         resistance4 = pivot + 6.854 * (high - low)
    #         resistance5 = pivot + 11.090 * (high - low)          
            
    #         latest_pivot_dict = {
    #             'pp': pivot.iloc[-1],
    #             'S1': support1.iloc[-1],
    #             'S2': support2.iloc[-1],
    #             'S3': support3.iloc[-1],
    #             'S4': support4.iloc[-1], 
    #             'S5': support5.iloc[-1],  
    #             # 'S6': support6.iloc[-1],
    #             # 'S7': support7.iloc[-1],
    #             'R1': resistance1.iloc[-1],
    #             'R2': resistance2.iloc[-1],
    #             'R3': resistance3.iloc[-1],
    #             'R4': resistance4.iloc[-1], 
    #             'R5': resistance5.iloc[-1],
    #             # 'R6': resistance6.iloc[-1],
    #             # 'R7': resistance7.iloc[-1]   
    #         }
    #         # self.pivot_levels_type = 6  # Update the number of pivot levels
    #         piv_repl = {
    #             f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
    #             f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
    #         }
    #     except Exception as ex:
    #         print(ex)

    #     return piv_repl

    # def calculate_classic_pivot_points(self, data):
    #     data = data.iloc[-30:]
    #     latest_pivot_dict = {}
    #     piv_repl = {} 
    #     try:
    #         high = data['High']
    #         low = data['Low']
    #         close = data['Close']

    #         pivot = (high + low + close) / 3
    #         # support1 = (2 * pivot) - high
    #         # support2 = pivot - (high - low)
    #         # support2 = pivot - 2 * (high - low)
    #         support1 = pivot - 3 * (high - low)
    #         support2 = pivot - 4 * (high - low)  
    #         support3 = pivot - 5 * (high - low)
    #         support4 = pivot - 6 * (high - low)
    #         support5 = pivot - 7 * (high - low)  
    #         # resistance1 = (2 * pivot) - low
    #         # resistance2 = pivot + (high - low)
    #         # resistance3 = pivot + 2 * (high - low)
    #         # resistance4 = pivot + 3 * (high - low)  
    #         resistance1 = pivot + 3 * (high - low)
    #         resistance2 = pivot + 4 * (high - low)
    #         resistance3 = pivot + 5 * (high - low)
    #         resistance4 = pivot + 6 * (high - low)
    #         resistance5 = pivot + 7 * (high - low)  
            
    #         latest_pivot_dict = {
    #             'pp': pivot.iloc[-1],
    #             'S1': support1.iloc[-1],
    #             'S2': support2.iloc[-1],
    #             'S3': support3.iloc[-1],
    #             'S4': support4.iloc[-1], 
    #             'S5': support5.iloc[-1],  
    #             # 'S6': support6.iloc[-1],
    #             # 'S7': support7.iloc[-1],
    #             'R1': resistance1.iloc[-1],
    #             'R2': resistance2.iloc[-1],
    #             'R3': resistance3.iloc[-1],
    #             'R4': resistance4.iloc[-1], 
    #             'R5': resistance5.iloc[-1],
    #             # 'R6': resistance6.iloc[-1],
    #             # 'R7': resistance7.iloc[-1]   
    #         }
    #         # self.pivot_levels_type = 4  # Update the number of pivot levels
    #         piv_repl = {
    #             f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
    #             f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
    #         }
    #     except Exception as ex:
    #         print(f"str31: {ex}")

    #     return piv_repl

    # def calculate_manualy_pivot(self, data):
    #     piv = None
    #     if self.PIVOT_GENERAL_TYPE == 'Classic':
    #         piv = self.calculate_classic_pivot_points(data)
    #     elif self.PIVOT_GENERAL_TYPE == 'Fibonacci':
    #         piv = self.calculate_fibonacci_pivot_points(data)

    #     return piv

    # def calculate_finta_pivot(self, dataa, period=30):
    #     # finta
    #     # dataa = data.copy()
    #     piv_repl = {}
    #     piv = None
   
    #     if self.PIVOT_GENERAL_TYPE == 'Classic':
    #         piv = TA.PIVOT(dataa)
    #     elif self.PIVOT_GENERAL_TYPE == 'Fibonacci':
    #         piv = TA.PIVOT_FIB(dataa)

    #     latest_pivot = piv.iloc[-period:]
    #     pivot_mean = latest_pivot.mean()
    #     latest_pivot_dict = {
    #         'pp': pivot_mean['pivot'],
    #         'S1': pivot_mean['s1'],
    #         'S2': pivot_mean['s2'],
    #         'S3': pivot_mean['s3'],
    #         'S4': pivot_mean['s4'],
         
    #         'R1': pivot_mean['r1'],
    #         'R2': pivot_mean['r2'],
    #         'R3': pivot_mean['r3'],
    #         'R4': pivot_mean['r4']            
    #     }
    #     # self.pivot_levels_type = 4
    #     piv_repl = {
    #         f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.S{self.pivot_levels_type}': latest_pivot_dict[f'S{self.pivot_levels_type}'],
    #         f'Pivot.M.{self.PIVOT_GENERAL_TYPE}.R{self.pivot_levels_type}': latest_pivot_dict[f'R{self.pivot_levels_type}']
    #     }

    #     return piv_repl


    # def sl_generator_two(self, data):
    #     SL_Signal = [0] * len(data)
    #     TP_Signal = [0] * len(data)
    #     SLbackcandles = 30

    #     for row in range(SLbackcandles, len(data)):
    #         defender = data['ordersignal'].iloc[row]
    #         if data['ordersignal'].iloc[row] == 2 or data['ordersignal'].iloc[row] == 1:                
    #             sl, tp = self.sl_tp_calculations(data.iloc[:row], defender)
    #             SL_Signal[row] = sl
    #             TP_Signal[row] = tp
                
    #     data.loc[:, 'SLSignal'] = SL_Signal
    #     data.loc[:, 'TPSignal'] = TP_Signal
    #     # data.loc[:, 'SL_S_Signal'] = SL_S_Signal
    #     # data.loc[:, 'TP_S_Signal'] = TP_S_Signal
    #     # print(data.loc[:, 'TPSignal'].to_list())
    #     return data




        # def next(self):
        #     super().next()
        #     self.mysize = 0.01

            # if mainn_init.sl_strategy == 1:
            #     for trade in self.trades:
            #         # pass
            #         if trade.is_long:
            #             trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
            #         else:
            #             trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr)
            # if self.signal1[-1] == 2 and len(self.trades) == 0:

            #     if mainn_init.sl_strategy == 1:
            #         sl1 = mainn_init.sl_generator_one(self.data, self.signal1[-1])
            #         try:
            #             self.buy(sl=sl1, size=self.mysize)
            #         except Exception as ex:
            #             print(ex)
            #     if mainn_init.sl_strategy == 2:
            #         sl1, tp1 = mainn_init.sl_generator_two(self.data, self.signal1[-1])
            #         try:
            #             self.buy(sl=sl1, tp=tp1, size=self.mysize)
            #         except Exception as ex:
            #             print(ex)

            #     if mainn_init.sl_strategy == 3:
            #         sl1, tp1 = mainn_init.sl_generator_three(self.data, self.signal1[-1])
            #         try:
            #             self.buy(sl=sl1, tp=tp1, size=self.mysize)
            #         except Exception as ex:
            #             print(ex)


            # elif self.signal1[-1] == 1 and len(self.trades) == 0: 
            # # if self.data.bollinger_engulfing_signal[-1] == 1 and len(self.trades) == 0:
            #     # print(self.data.bollinger_engulfing_signal)
            #     if mainn_init.sl_strategy == 1:
            #         sl1 = mainn_init.sl_generator_one(self.data, self.signal1[-1])
            #         try:
            #             self.sell(sl=sl1, size=self.mysize)
            #         except:
            #             pass
            #     if mainn_init.sl_strategy == 2:
            #         sl1, tp1 = mainn_init.sl_generator_two(self.data, self.signal1[-1])
            #         try:
            #             self.sell(sl=sl1, tp=tp1, size=self.mysize)
            #         except Exception as ex:
            #             print(ex)

            #     if mainn_init.sl_strategy == 3:
            #         sl1, tp1 = mainn_init.sl_generator_three(self.data, self.signal1[-1])
            #         try:
            #             self.sell(sl=sl1, tp=tp1, size=self.mysize)
            #         except Exception as ex:
            #             print(ex)
    

        # def next(self):
        #     super().next()
        #     TPSLRatio = 1
            
        #     #if len(self.trades)>0:            
        #     #    if self.trades[-1].is_long and self.data.RSI[-1]>=70:
        #     #        self.trades[-1].close()
        #     #    elif self.trades[-1].is_short and self.data.RSI[-1]<=30:
        #     #        self.trades[-1].close()
                    
        #     if len(self.trades)>0:            
        #         if self.trades[-1].is_long and self.data.Heiken_Open[-1]>=self.data.Heiken_Close[-1]:
        #             self.trades[-1].close()
        #         elif self.trades[-1].is_short and self.data.Heiken_Open[-1]<=self.data.Heiken_Close[-1]:
        #             self.trades[-1].close()
            
        #     if self.signal1==2 and len(self.trades)==0:   
        #         sl1 = self.data.SLSignal[-1]
        #         tp1 = self.data.Close[-1]+(self.data.Close[-1] - sl1)*TPSLRatio
        #         self.buy(sl=sl1, tp=tp1, size=self.mysize)
            
        #     elif self.signal1==1 and len(self.trades)==0:         
        #         sl1 = self.data.SLSignal[-1]
        #         tp1 = self.data.Close[-1]-(sl1 - self.data.Close[-1])*TPSLRatio
        #         self.sell(sl=sl1, tp=tp1, size=self.mysize)


# /////////////////////// 3 ///////////////////////////////////////////////

        # def next(self):
        #     super().next()
        #     TPSLRatio = 1.618

        #     if self.signal1==2 and len(self.trades)==0:   
        #         sl1 = min(self.data.Low[-2], self.data.Low[-1])
        #         tp1 = self.data.Close[-1] + abs(self.data.Close[-1]-sl1)*TPSLRatio
        #         self.buy(sl=sl1, tp=tp1, size=self.mysize)
            
        #     elif self.signal1==1 and len(self.trades)==0:         
        #         sl1 = max(self.data.High[-2], self.data.High[-1])
        #         tp1 = self.data.Close[-1] - abs(sl1-self.data.Close[-1])*TPSLRatio
        #         self.sell(sl=sl1, tp=tp1, size=self.mysize)