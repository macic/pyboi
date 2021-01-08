import numpy as np
import pandas as pd

def np_array_to_ohlc_df(klines: np.core.multiarray) -> pd.DataFrame:
    df = pd.DataFrame(klines.reshape(-1,6),dtype=float, columns = ('ts',
                                                                    'open',
                                                                    'high',
                                                                    'low',
                                                                    'close',
                                                                    'volume'))


    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    #df.set_index('Open Time')
    return df

