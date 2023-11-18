# import yfinance as yf
# import pandas_ta as tafrom 
# import math

# def get_historical_data(symbol):
#     data = yf.download(tickers = symbol, start = '2012-03-11',end = '2022-07-10')
#     data.drop(['Volume'], axis=1, inplace=True)
#     data.head(10)
#     return data



# def HeikenSignal1(df):
#     signal1=[0]*len(df)
#     # signal1=[0 for i in rqnge(len(df))]
#     for i in range(1, len(df)):
#         #df.Heiken_High[i-1]<=df.Heiken_Open[i-1])and
#         PreviousHeikenBody = math.fabs(df.Heiken_Open[i-1]-df.Heiken_Close[i-1])
#         ratio = 1.5
#         if ( 
#             (df.Heiken_High[i-1]-max(df.Heiken_Open[i-1], df.Heiken_Close[i-1]))
#             /PreviousHeikenBody>ratio and
#             (min(df.Heiken_Open[i-1], df.Heiken_Close[i-1]) - df.Heiken_Low[i-1])
#             /PreviousHeikenBody>ratio and
#             (df.Heiken_Open[i]<df.Heiken_Close[i] and df.Heiken_Low[i]>=df.Heiken_Open[i]) ):
#             signal1[i]=2
#         #df.Heiken_High[i-1]<=df.Heiken_Open[i-1])and
#         if ( (df.Heiken_High[i-1]-max(df.Heiken_Open[i-1], df.Heiken_Close[i-1]))
#             /PreviousHeikenBody>ratio>ratio and
#             (min(df.Heiken_Open[i-1], df.Heiken_Close[i-1]) - df.Heiken_Low[i-1])
#             /PreviousHeikenBody>ratio>ratio and
#             (df.Heiken_Open[i]>df.Heiken_Close[i] and df.Heiken_High[i]<=df.Heiken_Open[i]) ):
#             signal1[i]=1
#     df['HeikenSignal1'] = signal1
    
# def totalSignal(df):
#     ordersignal=[0]*len(df)
#     for i in range(0, len(df)):
#         if (df.EMA10[i]>df.EMA30[i] and df.Heiken_Open[i]<df.EMA10[i] 
#             and df.Heiken_Close[i]>df.EMA10[i] 
#             and df.HeikenSignal1[i] == 2):
#             ordersignal[i]=2
#         if (df.EMA10[i]<df.EMA30[i] and df.Heiken_Open[i]>df.EMA10[i] 
#             and df.Heiken_Close[i]<df.EMA10[i]
#             and df.HeikenSignal1[i] == 1):
#             ordersignal[i]=1
#     df['ordersignal']=ordersignal
# HeikenSignal1(data)
# totalSignal(data)

# data.dropna(inplace=True)
# data.reset_index(inplace=True)
# data

# import numpy as np
# def pointpos(x):
#     if x['ordersignal']==1:
#         return x['High']+1e-4
#     elif x['ordersignal']==2:
#         return x['Low']-1e-4
#     else:
#         return np.nan
# data['pointpos'] = df=data.apply(lambda row: pointpos(row), axis=1)

# dfpl = data[2000:2100]
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Heiken_Open'],
#                 high=dfpl['Heiken_High'],
#                 low=dfpl['Heiken_Low'],
#                 close=dfpl['Heiken_Close']),
#                      go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
#                      go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

# fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
#                 marker=dict(size=5, color="MediumPurple"),
#                 name="Signal")
# fig.show()

# dfpl = data[2100:2200]
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['Open'],
#                 high=dfpl['High'],
#                 low=dfpl['Low'],
#                 close=dfpl['Close']),
#                      go.Scatter(x=dfpl.index, y=dfpl.EMA10, line=dict(color='red', width=1), name="EMA10"),
#                      go.Scatter(x=dfpl.index, y=dfpl.EMA30, line=dict(color='blue', width=1), name="EMA30")])

# fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
#                 marker=dict(size=5, color="MediumPurple"),
#                 name="Signal")
# fig.show()


# # StopLoss from signal
# SLSignal = [0] * len(df)
# SLbackcandles = 1
# for row in range(SLbackcandles, len(data)):
#     mi=1e10
#     ma=-1e10
#     if data.ordersignal[row]==1:
#         for i in range(row-SLbackcandles, row+1):
#             ma = max(ma,data.High[i])
#         SLSignal[row]=ma
#     if data.ordersignal[row]==2:
#         for i in range(row-SLbackcandles, row+1):
#             mi = min(mi,data.Low[i])
#         SLSignal[row]=mi
        
# data['SLSignal']=SLSignal

# dfpl = df[:]
# def SIGNAL():
#     return dfpl.ordersignal


# dfpl = data[:]
# from backtesting import Strategy
# from backtesting import Backtest

# class MyStrat(Strategy):
#     initsize = 0.2
#     mysize = initsize
#     def init(self):
#         super().init()
#         self.signal1 = self.I(SIGNAL)

#     def next(self):
#         super().next()
#         TPSLRatio = 1
        
#         #if len(self.trades)>0:            
#         #    if self.trades[-1].is_long and self.data.RSI[-1]>=70:
#         #        self.trades[-1].close()
#         #    elif self.trades[-1].is_short and self.data.RSI[-1]<=30:
#         #        self.trades[-1].close()
                   
#         if len(self.trades)>0:            
#             if self.trades[-1].is_long and self.data.Heiken_Open[-1]>=self.data.Heiken_Close[-1]:
#                 self.trades[-1].close()
#             elif self.trades[-1].is_short and self.data.Heiken_Open[-1]<=self.data.Heiken_Close[-1]:
#                 self.trades[-1].close()
        
#         if self.signal1==2 and len(self.trades)==0:   
#             sl1 = self.data.SLSignal[-1]
#             tp1 = self.data.Close[-1]+(self.data.Close[-1] - sl1)*TPSLRatio
#             self.buy(sl=sl1, tp=tp1, size=self.mysize)
        
#         elif self.signal1==1 and len(self.trades)==0:         
#             sl1 = self.data.SLSignal[-1]
#             tp1 = self.data.Close[-1]-(sl1 - self.data.Close[-1])*TPSLRatio
#             self.sell(sl=sl1, tp=tp1, size=self.mysize)

# bt = Backtest(dfpl, MyStrat, cash=10000, margin=1/50, commission=.00)
# stat = bt.run()
# stat

# bt.plot(show_legend=False)


# # from backtesting import Strategy, Backtest
# # import numpy as np

# # class MyCandlesStrat(Strategy):
# #     sltr = 1
# #     mysize = 0.1
# #     def init(self):
# #         super().init()
# #         self.signal1 = self.I(SIGNAL)

# #     def next(self):
# #         super().next()
# #         sltr = self.sltr
# #         for trade in self.trades: 
# #             if trade.is_long: 
# #                 trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
# #             else:
# #                 trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr) 

# #         if self.signal1==2 and len(self.trades)==0:
# #             self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
# #             sl1 = self.data.Close[-1] - self.sltr
# #             self.buy(sl=sl1, size=self.mysize)
# #         elif self.signal1==1 and len(self.trades)==0:
# #             self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
# #             sl1 = self.data.Close[-1] + self.sltr
# #             self.sell(sl=sl1, size=self.mysize)

# # bt = Backtest(dfpl, MyCandlesStrat, cash=10000, margin=1/50, commission=.00)
# # stat = bt.run()
# # stat

# # bt.plot(show_legend=False)


# def main(symbol, slicee):
#     mainn_init = MAIN_INIT()
#     mainn_init.go_(symbol, slicee)

#     class MyCandlesStrat(Strategy):
#         sltr = 1
#         mysize = 0.1

#         def init(self):
#             super().init()
#             self.signal1 = self.I(mainn_init.SIGNAL)

#         def next(self):
#             super().next()
#             sltr = self.sltr

#             for trade in self.trades:
#                 if trade.is_long:
#                     trade.sl = max(trade.sl or -np.inf, self.data.Close[-1] - self.sltr)
#                 else:
#                     trade.sl = min(trade.sl or np.inf, self.data.Close[-1] + self.sltr)

#             if self.signal1[-1] == 2 and len(self.trades) == 0:
#                 self.sltr = self.data.Close[-1] - self.data.SLSignal[-1]
#                 sl1 = self.data.Close[-1] - self.sltr
#                 self.buy(sl=sl1, size=self.mysize)

#             elif self.signal1[-1] == 1 and len(self.trades) == 0:
#                 self.sltr = self.data.SLSignal[-1] - self.data.Close[-1]
#                 sl1 = self.data.Close[-1] + self.sltr
#                 self.sell(sl=sl1, size=self.mysize)

#     # Convert the index to a simple period index
#     mainn_init.dfpl.index = pd.RangeIndex(len(mainn_init.dfpl))

#     bt = Backtest(mainn_init.dfpl, MyCandlesStrat, cash=10000, margin=1/50, commission=.001)
#     stat = bt.run()
#     print(stat)


# def calculate_metrics(equity_curve, trades):
#     # Calculate key metrics
#     start = 0
#     end = len(equity_curve) - 1
#     duration = end - start
#     exposure_time_pct = (np.count_nonzero(trades) / duration) * 100
#     equity_final = equity_curve[end]

#     # Avoid division by zero or invalid values
#     if equity_curve[start] != 0:
#         return_pct = ((equity_final / equity_curve[start]) - 1) * 100
#         buy_and_hold_return_pct = ((equity_curve[end] / equity_curve[start]) - 1) * 100
#         return_annualized = ((1 + return_pct / 100) ** (1 / (duration / 365.25)) - 1) * 100
#         max_drawdown_pct = ((np.min(equity_curve[start:end]) / equity_curve[start]) - 1) * 100
#     else:
#         return_pct = 0
#         buy_and_hold_return_pct = 0
#         return_annualized = 0
#         max_drawdown_pct = 0

#     returns_diff = np.diff(equity_curve[start:end]) / equity_curve[start:end][1:]

#     if len(returns_diff) > 1 and not np.any(equity_curve[start:end][:-1] == 0):
#         volatility_annualized = np.nanstd(returns_diff) * np.sqrt(252) * 100
#     else:
#         volatility_annualized = np.nan

#     sharpe_ratio = (return_annualized - 0) / volatility_annualized if volatility_annualized != 0 else np.nan
#     sortino_ratio = (return_annualized - 0) / np.std(np.minimum(0, returns_diff)) * np.sqrt(252) if np.min(returns_diff) < 0 else np.nan
#     calmar_ratio = return_annualized / abs(np.min(equity_curve[start:end]) / equity_curve[start]) if np.min(equity_curve[start:end]) < 0 else np.nan
#     avg_drawdown_pct = np.nanmean(equity_curve[start:end] - np.maximum.accumulate(equity_curve[start:end])) / np.nanmean(equity_curve[start:end]) * 100 if not np.isnan(np.nanmean(equity_curve[start:end] - np.maximum.accumulate(equity_curve[start:end]))) and not np.isnan(np.nanmean(equity_curve[start:end])) else np.nan
#     max_drawdown_duration = np.argmax(np.maximum.accumulate(equity_curve[start:end]) - equity_curve[start:end])  # This gives the index of the maximum drawdown
#     avg_drawdown_duration = np.nanmean(np.diff(np.where(np.maximum.accumulate(equity_curve[start:end]) - equity_curve[start:end] == 0))) if max_drawdown_duration > 0 else np.nan

#     num_trades = np.count_nonzero(trades)
#     win_rate_pct = (np.count_nonzero(trades > 0) / num_trades) * 100 if num_trades > 0 else np.nan
#     best_trade_pct = np.max(trades) if np.max(trades) > 0 else np.nan
#     worst_trade_pct = np.min(trades) if np.min(trades) < 0 else np.nan
#     avg_trade_pct = np.nanmean(trades)
#     max_trade_duration = np.nan
#     avg_trade_duration = np.nan
#     profit_factor = np.sum(trades[trades > 0]) / abs(np.sum(trades[trades < 0])) if np.sum(trades[trades < 0]) != 0 else np.nan
#     expectancy_pct = np.nanmean(trades) if num_trades > 0 else np.nan
#     sqn = np.nan

#     return {
#         "Start": start,
#         "End": end,
#         "Duration": duration,
#         "Exposure Time [%]": exposure_time_pct,
#         "Equity Final [$]": equity_final,
#         "Return [%]": return_pct,
#         "Buy & Hold Return [%]": buy_and_hold_return_pct,
#         "Return (Ann.) [%]": return_annualized,
#         "Volatility (Ann.) [%]": volatility_annualized,
#         "Sharpe Ratio": sharpe_ratio,
#         "Sortino Ratio": sortino_ratio,
#         "Calmar Ratio": calmar_ratio,
#         "Max. Drawdown [%]": max_drawdown_pct,
#         "Avg. Drawdown [%]": avg_drawdown_pct,
#         "Max. Drawdown Duration": max_drawdown_duration,
#         "Avg. Drawdown Duration": avg_drawdown_duration,
#         "# Trades": num_trades,
#         "Win Rate [%]": win_rate_pct,
#         "Best Trade [%]": best_trade_pct,
#         "Worst Trade [%]": worst_trade_pct,
#         "Avg. Trade [%]": avg_trade_pct,
#         "Max. Trade Duration": max_trade_duration,
#         "Avg. Trade Duration": avg_trade_duration,
#         "Profit Factor": profit_factor,
#         "Expectancy [%]": expectancy_pct,
#         "SQN": sqn,
#     }

# def main(symbol, slicee):
#     mainn_init = MAIN_INIT()
#     mainn_init.go_(symbol, slicee)

#     # Convert the index to a simple period index
#     mainn_init.dfpl.index = pd.RangeIndex(len(mainn_init.dfpl))

#     sltr = 1
#     mysize = 0.1

#     equity = 10000
#     margin = 1/50
#     commission = 0.001
#     trades = []
#     orders = mainn_init.dfpl['ordersignal'].to_numpy()
#     equity_curve = np.zeros(len(mainn_init.dfpl))

#     for i, row in mainn_init.dfpl.iterrows():
#         if orders[i] == 2 and len(trades) == 0:
#             sltr = row['Close'] - row['SLSignal']
#             sl1 = row['Close'] - sltr
#             trades.append({'entry': i, 'sl': sl1, 'size': mysize, 'type': 'buy'})
#             equity -= sl1 * mysize * margin + commission
#         elif orders[i] == 1 and len(trades) == 0:
#             sltr = row['SLSignal'] - row['Close']
#             sl1 = row['Close'] + sltr
#             trades.append({'entry': i, 'sl': sl1, 'size': mysize, 'type': 'sell'})
#             equity -= sl1 * mysize * margin + commission

#         for trade in trades:
#             if trade['type'] == 'buy':
#                 trade['sl'] = max(trade['sl'], row['Close'] - sltr)
#                 equity += row['Close'] * trade['size'] * margin - commission
#             elif trade['type'] == 'sell':
#                 trade['sl'] = min(trade['sl'], row['Close'] + sltr)
#                 equity += row['Close'] * trade['size'] * margin - commission

#         equity_curve[i] = equity

#     # Calculate and print the financial metrics
#     metrics = calculate_metrics(equity_curve, mainn_init.dfpl['ordersignal'].to_numpy())
#     for key, value in metrics.items():
#         print(f"{key}: {value}")


