import os
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
from binance.client import Client
from time import time
api_key = os.getenv('binance_key')
api_secret = os.getenv('binance_secret')
#client = Client(api_key, api_secret)

#x=client.get_asset_balance('EUR')
#print(float(x.get('free', 0)))
from utils.database import session_scope, engine
from models.symbol import Etheur


with session_scope() as session:

    pandas_data = pd.read_sql_table('etheur', engine)
    # data = Etheur.get_from_last_year()

    pandas_data = pandas_data.sort_values(by=['ts'])
    pandas_data.index = pd.to_datetime(pandas_data.ts, unit='s')
    #pandas_data.ts = pandas_data.index


    df = pandas_data.resample('D').agg({'open': 'first',
                           'high': 'max',
                           'low': 'min',
                           'close': 'last',
                           'volume': 'sum'})
    #print(df)

    index_names = pandas_data[(pandas_data['ts'] < '2021-01-13 00:00:00')].index

    # drop these given row
    # indexes from dataFrame
    pandas_data.drop(index_names, inplace=True)

    from talib.abstract import *
    import talib
    #candle_indicator = CDLMARUBOZU(df)
    candle_indicator = CDLENGULFING(pandas_data)
    print("pattern detection")
    for index, value in candle_indicator.items():
        if value!=0:
            print(index, value)
    #raise
    df = pandas_data
    indicator = KAMA(df, 10, 2, 30)
    indicator_2 = KAMA(df, 20, 2, 30)
    #indicator = SMA(df, 25)
    bbands= BBANDS(df, 20, 2.0, 2.0)
    #print(indicator)
    #print(bbands)
    hovertext = []
    for i in range(len(df['open'])):
        hovertext.append('Open: ' + str(df['open'][i]) + '<br>High: ' + str(df['high'][i])+ '<br>Low: ' + str(df['low'][i])+ '<br>Close: ' + str(df['close'][i]))

    set1 = dict(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                text=hovertext,
                hoverinfo='text',
                type='candlestick')
    set2= {'x': bbands.index,
           'y': bbands['upperband'],
           'type': 'scatter',
           'mode': 'lines',
           'line': {'width': 1, 'color': 'blue'},
           'name': 'BBAnds upper'}
    set3 = {'x': indicator.index,
            'y': indicator,
            'type': 'scatter',
            'mode': 'lines',
            'line': {'width': 1, 'color': 'orange'},
            'name': 'KAMA'}

    set4 = {'x': indicator_2.index,
            'y': indicator_2,
            'type': 'scatter',
            'mode': 'lines',
            'line': {'width': 1, 'color': 'navy'},
            'name': 'KAMA'}
    layout = go.Layout({'title':'ETHEUR Daily', 'font': {'size': 25}})
    data=[set1, set3, set4]
    fig = go.Figure(data=data, layout=layout)
    fig.show()



    #print(session.query(Etheur).first())
    #print(session.query(Etheur).all())
#
# def binanceDataFrame(klines):
#     df = pd.DataFrame(klines.reshape(-1,12),dtype=float, columns = ('Open Time',
#                                                                     'Open',
#                                                                     'High',
#                                                                     'Low',
#                                                                     'Close',
#                                                                     'Volume',
#                                                                     'Close time',
#                                                                     'Quote asset volume',
#                                                                     'Number of trades',
#                                                                     'Taker buy base asset volume',
#                                                                     'Taker buy quote asset volume',
#                                                                     'Ignore'))
#
#     df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
#
#
#     return df
#
# klines = np.array(client.get_historical_klines("ETHEUR", Client.KLINE_INTERVAL_5MINUTE, "1 hour ago UTC"))
# print(klines)
# print("\nDATAFRAME\n")
# print(binanceDataFrame(klines))
# get market depth
# depth = client.get_order_book(symbol='ETHEUR',limit=5)
# print (depth)

# place a test market buy order, to place an actual order use the create_order function
# order = client.create_test_order(
#     symbol='BNBBTC',
#     side=Client.SIDE_BUY,
#     type=Client.ORDER_TYPE_MARKET,
#     quantity=100)
#
#
# # get all symbol prices
# prices = client.get_all_tickers()
# print(prices)
#
#
# # withdraw 100 ETH
# # check docs for assumptions around withdrawals
# from binance.exceptions import BinanceAPIException, BinanceWithdrawException
# try:
#     result = client.withdraw(
#         asset='ETH',
#         address='<eth_address>',
#         amount=100)
# except BinanceAPIException as e:
#     print(e)
# except BinanceWithdrawException as e:
#     print(e)
# else:
#     print("Success")
#
# # fetch list of withdrawals
# withdraws = client.get_withdraw_history()
#
# # fetch list of ETH withdrawals
# eth_withdraws = client.get_withdraw_history(asset='ETH')
#
# # get a deposit address for BTC
# address = client.get_deposit_address(asset='BTC')
#
# # start aggregated trade websocket for BNBBTC
# def process_message(msg):
#     print("message type: {}".format(msg['e']))
#     print(msg)
#     # do something
#
# from binance.websockets import BinanceSocketManager
# bm = BinanceSocketManager(client)
# bm.start_aggtrade_socket('BNBBTC', process_message)
# bm.start()
#
# # get historical kline data from any date range
#
# # fetch 1 minute klines for the last day up until now
# klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
#
# # fetch 30 minute klines for the last month of 2017
# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
#
# # fetch weekly klines since it listed
# klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

