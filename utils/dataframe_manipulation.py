import pandas as pd
def binanceDataFrame(klines):
    df = pd.DataFrame(klines.reshape(-1,6),dtype=float, columns = ('Open Time',
                                                                    'Open',
                                                                    'High',
                                                                    'Low',
                                                                    'Close',
                                                                    'Volume'))

    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')

    return df

