
class SL_STRATEGY_TWOO():

    def __init__(self) -> None:
        super().__init__()
        
    def calculate_atr(self, data, period=14):
        true_ranges = []
        for i in range(1, len(data)):
            high = data['High'][i]
            low = data['Low'][i]
            close = data['Close'][i - 1]
            true_range = max(abs(high - low), abs(high - close), abs(low - close))        
            true_ranges.append(true_range)
        atr = sum(true_ranges[-period:]) / period

        return atr

    def sl_generator_two(self, data, defender):
        sl, tp = None, None
        atr = self.calculate_atr(data)
        l_pr = data['Close'][-1]
        # 0.9 1.2
        # 1 1.382
        # 1 1.618
        if defender == 2:
            tp, sl = l_pr + atr*1.382, l_pr - atr*1
            # print(f"sl_L_level: {sl}, close_price: {l_pr}, tp_L_level: {tp}")
            if sl >= tp or tp <= l_pr or sl >= l_pr:
                raise ValueError("For a long order, SL should be less than TP.")         

        elif defender == 1:
            sl, tp = l_pr + atr*1, l_pr - atr*1.382
            # print(f"sl_S_level: {sl}, close_price: {l_pr}, tp_S_level: {tp}")
            if sl <= tp or tp >= l_pr or sl <= l_pr:
                raise ValueError("For a long order, SL should be less than TP.")  
        
        return sl, tp







# ghf = SL_STRATEGY_TWO()

# python -m SL_STRATEGYES.sl_2
