import numpy as np
from binance.client import Client
from config.base import api_key, api_secret
from sqlalchemy.types import DateTime, Numeric
from utils.session import engine
from utils.dataframe_manipulation import np_array_to_ohlc_df
from utils.logger import logger

client = Client(api_key, api_secret)


def replace_into(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    stmt = insert(table.table).values(data)
    stmt = stmt.on_conflict_do_update(index_elements=['ts'],
                                      set_=dict(open=stmt.excluded.open,
                                                close=stmt.excluded.close,
                                                high=stmt.excluded.high,
                                                low=stmt.excluded.low,
                                                volume=stmt.excluded.volume))

    conn.execute(stmt)


def scrape(symbol, start_str='1 day ago UTC', end_str=None):
    klines = np.array(
        client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE,
                                     start_str=start_str,
                                     end_str=end_str, limit=1000)
    )
    # remove everything besides Time+OHLC+Volume
    if len(klines) > 0:
        klines = np.delete(klines, np.s_[6:12], 1)

        # cast to dataframe
        df = np_array_to_ohlc_df(klines)

        # defining table name
        table_name = symbol.lower()

        # save to db
        df.to_sql(
            table_name,
            engine,
            if_exists='append',
            index=False,
            chunksize=500,
            dtype={
                "ts": DateTime,
                "open": Numeric,
                "high": Numeric,
                "low": Numeric,
                "close": Numeric,
                "volume": Numeric
            },
            method=replace_into
        )
        quantity = len(klines)
        logger.success(f"klines inserted into DB, quantity: {quantity}")
