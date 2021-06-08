import baker
from backtester.core import BackTester

from api_wrapper.core import BackTesterAPIClient, BinanceAPIClient
from scraper.core import scrape
from utils.logger import logger
from utils.database import engine

@logger.catch
@baker.command
def run_scraper(symbol='ETHEUR', start_month_before=1, end_month_before=None):
    start_str=f'{start_month_before} month ago UTC'
    end_str=f'{end_month_before} month ago UTC' if end_month_before else None

    logger.info(f"scraper monthly started for {symbol} - months before: {start_month_before}.")
    scrape(symbol, start_str=start_str, end_str=end_str)

@logger.catch
@baker.command
def run_cron_updater(symbol='ETHEUR', start_minutes_before=3):
    start_str=f'{start_minutes_before} minute ago UTC'

    logger.info(f"cron started for {symbol} using {start_minutes_before} minutes window.")
    scrape(symbol, start_str=start_str)

@baker.command
def run_backtest(symbol='ETHEUR'):
    import pandas as pd
    df = pd.read_sql_table('etheur', engine)
    count = len(df)

    logger.info(f"table data read for symbol: {symbol} total: {count}.")
    # create backtester API client
    client = BackTesterAPIClient(symbol=symbol)

    logger.info("start running backtest")

    # run Strategy processor
    bt =BackTester(symbol=symbol, strategy_class='TestStrategy', indicators=[], df=df, client = client)
    bt.process()

@baker.command
def process(symbol='ETHEUR'):
    import pandas as pd
    df = pd.read_sql_table('etheur', engine)
    count = len(df)

    logger.info(f"table data read for symbol: {symbol} total: {count}.")
    # create real API client
    client = BinanceAPIClient(symbol=symbol)

    logger.info(f"start running real processing for {symbol}")

    # run Strategy processor
    bt = BackTester(symbol=symbol, strategy_class='TestStrategy', indicators=[], df=df, client = client)
    bt.process()

baker.run()
