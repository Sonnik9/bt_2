
class SL_STRATEGY_THREE():

    def __init__(self) -> None:
        super().__init__()        

    def sl_generator_three(self, data, defender):
        sl1, tp1 = None, None
        TPSLRatio = 1.5
        if defender == 2:                
            sl1 = min(data.Low[-2], data.Low[-1])
            tp1 = data.Close[-1] + abs(data.Close[-1]-sl1)*TPSLRatio
            
        if defender == 1:               
            sl1 = max(data.High[-2], data.High[-1])
            tp1 = data.Close[-1] - abs(sl1-data.Close[-1])*TPSLRatio
            
        return sl1, tp1