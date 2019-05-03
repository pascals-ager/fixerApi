from pathlib import Path
import os


def singleton(cls, *args, **kwargs):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            return instances[cls]
    return _singleton


@singleton
class ApiConfiguration(object):
    api_key = '@@'


@singleton
class ServiceConfiguration(object):
    host = 'https://data.fixer.io/api'
    table_name = 'HISTORICAL_CURRENCY_RATES'
    db_name = 'currencyRates.db'


@singleton
class DbConfiguration(object):
    home = str(Path.home())
    path = os.path.join(home, 'sqlite')
    username = 'currencyRates'
    password = ''
