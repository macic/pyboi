import baker
from scraper.core import scrape
from utils.logger import logger

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


baker.run()
