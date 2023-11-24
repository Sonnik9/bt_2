from IND_STRATEGIES.ind_1 import HEIKEN_ASHI_PATTERN
from IND_STRATEGIES.ind_2 import BB_DOJI_ENGULGING_PATTERN
from SL_STRATEGYES.sl_1 import SL_STRATEGY_ONE
from SL_STRATEGYES.sl_2 import SL_STRATEGY_TWOO
from SL_STRATEGYES.sl_3 import SL_STRATEGY_THREE

class SL_INIT(BB_DOJI_ENGULGING_PATTERN, HEIKEN_ASHI_PATTERN, SL_STRATEGY_ONE, SL_STRATEGY_TWOO, SL_STRATEGY_THREE):

    def __init__(self) -> None:
        super().__init__()

    def sl__init_func(self, data, defender):
        if self.sl_strategy == 1:    
            return self.sl_generator_one(data, defender)       

        if self.sl_strategy == 2: 
            self.sl_generator_two(data, defender)

        if self.sl_strategy == 3: 
            self.sl_generator_three(data, defender)
  
