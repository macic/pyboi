import baker
import numpy as np
from binance.client import Client
from config.base import api_key, api_secret
from sqlalchemy.types import DateTime, Numeric
from utils.session import session_scope, engine
from utils.dataframe_manipulation import np_array_to_ohlc_df

client = Client(api_key, api_secret)

def replace_into(table, conn, keys, data_iter):
    from sqlalchemy.dialects.postgresql import insert

    data = [dict(zip(keys, row)) for row in data_iter]

    stmt = insert(table.table).values(data)
    print(stmt.excluded)
    #stmt.on_isertpostgresql_insert_on_conflict()
    stmt = stmt.on_conflict_do_update(index_elements=['ts'],
                                             set_=dict(open=stmt.excluded.open,
                                                       close=stmt.excluded.close,
                                                       high=stmt.excluded.high,
                                                       low=stmt.excluded.low,
                                                       volume=stmt.excluded.volume))

    conn.execute(stmt)

@baker.command
def run(symbol='ETHEUR'):
    with session_scope() as session:
        klines = np.array(
            client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE , '1 hour ago UTC')
        )
        # remove everything besides Time+OHLC+Volume
        klines = np.delete(klines, np.s_[6:12], 1)

        # cast to dataframe
        df = np_array_to_ohlc_df(klines)

        print(df.index)
        print(df)
        # save to db

        table_name = symbol.lower()

        result =df.to_sql(
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

        print(result)



baker.run()