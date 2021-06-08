from typing import List

from binance.enums import SIDE_BUY
from pandas import DataFrame
from backtester.strategies import BaseStrategy, Signal
from api_wrapper.core import BaseClient
import backtester.strategies
from utils.logger import logger


class BackTester():

    def __init__(self, symbol: str, strategy_class: BaseStrategy, indicators: List, df: DataFrame, client: BaseClient):
        self.symbol = symbol
        self.strategy_class = strategy_class
        self.indicators = List
        self.df = df
        self.api_client = client

    def process(self):
        """
        1. check status of current trades
            a) if open - check if stop loss is met - if so close trade
            b) if open - check if take profit is met - if so close trade

            c) if pending to be open - ?
            d) if pending to be close - ?

            e) leave method don't continue to point 2

        2. if no currently open/pending trades - check if we should open one
            a) if we should open - create an order in proper direction and send it
            b) leave method

        """

        # point 1.

        # point 2. checking if we should open a trade
        strategy_class = getattr(backtester.strategies, self.strategy_class)
        Strategy = strategy_class()

        signal = Strategy.signal_open()
        if isinstance(signal, Signal):
            # check orderbook
            orderbook = self.api_client.get_orderbook()

            # determine price and quantity
            price, quantity = self._calculate_order_price_and_quantity(signal, orderbook)

            logger.info("orderbook")
            print(orderbook)
            # open limit order
            order = self.api_client.open_order(signal.direction, price, quantity)


    @classmethod
    def _calculate_order_price_and_quantity(cls, signal: Signal, orderbook):
        balance = cls.api_client.get_balance()
        if signal.direction == SIDE_BUY and len(orderbook.get('asks',[]))>0:
            best_ask = float(orderbook['asks'][0][0])

        price = 1
        quantity = 1
        return price, quantity

