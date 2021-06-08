import os
from binance.client import Client
from binance.enums import ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC


class BaseClient():
    def __init__(self, symbol):
        self.symbol = symbol

    def open_order(self, direction, price, quantity):
        raise NotImplementedError

    def close_order(self):
        raise NotImplementedError

    def get_orderbook(self):
        raise NotImplementedError

    def get_balance(self):
        raise NotImplementedError


class BackTesterAPIClient(BaseClient):
    """
    Used to run BackTests
    """

    def open_order(self, direction, price, quantity):
        return True

    def close_order(self):
        return True

    def get_orderbook(self):
        """
        {'lastUpdateId': 212939885, 'bids': [['1018.08000000', '0.09327000'], ['1017.62000000', '3.08881000'],
        ['1017.50000000', '0.14540000'], ['1017.46000000', '7.92999000'], ['1017.45000000', '11.25000000']],
        'asks': [['1018.42000000', '0.07502000'], ['1018.61000000', '0.50285000'], ['1018.62000000', '2.30769000'],
        ['1018.63000000', '0.97795000'], ['1018.71000000', '2.20949000']]}
        """
        return []

    def get_balance(self):
        return 1000


class BinanceAPIClient(BaseClient):
    """
    Wrapper for Binance API Python client
    """

    def __init__(self, *kwargs, **args):
        super().__init__(*kwargs, **args)
        api_key = os.getenv('binance_key')
        api_secret = os.getenv('binance_secret')
        self.client = Client(api_key, api_secret)

    def open_order(self, direction, price, quantity):
        return self.client.create_test_order(
            symbol=self.symbol,
            side=direction,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=price)

    def close_order(self):
        pass

    def get_orderbook(self):
        return self.client.get_order_book(symbol=self.symbol, limit=5)

    def get_balance(self):
        balance_response = self.client.get_asset_balance('EUR')
        return float(balance_response.get('free', 0))
