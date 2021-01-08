import baker
import numpy as np
from binance.client import Client
from config.base import api_key, api_secret
from utils.session import session_scope
from utils.dataframe_manipulation import binanceDataFrame

client = Client(api_key, api_secret)

@baker.command
def run(symbol='ETHEUR'):
    with session_scope() as session:
        klines = np.array(
            client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE , '1 hour ago UTC')
        )
        # remove everything besides Time+OHLC+Volume
        klines = np.delete(klines, np.s_[6:12], 1)
        # cast to dataframes
        print(binanceDataFrame(klines))

baker.run()