from collections import namedtuple
from typing import Optional
from binance.enums import SIDE_BUY, SIDE_SELL

Signal = namedtuple('Signal', ['direction', 'price'])


class BaseStrategy:

    def signal_open(self) -> Optional[Signal]:
        pass

    def close(self):
        pass


class TestStrategy(BaseStrategy):

    def signal_open(self) -> Optional[Signal]:
        print("open")
        return Signal(SIDE_BUY, None)

    def close(self):
        print("close")
        return True
