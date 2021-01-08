import os

api_key = os.getenv('binance_key')
api_secret = os.getenv('binance_secret')

db_host = os.getenv('pqsl_db_host')
db_user = os.getenv('pqsl_db_user')
db_pw = os.getenv('pqsl_db_pw')
db_name = os.getenv('pqsl_db_name')
db_url=f'postgresql://{db_user}:{db_pw}@{db_host}/{db_name}'

