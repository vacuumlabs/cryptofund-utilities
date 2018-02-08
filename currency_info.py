import requests
from datetime import datetime, timezone
import dateutil.parser
from memo import memo
import time

class ApiError(Exception):
    pass

@memo
def currency_info():
    data = requests.get(
        'https://api.coinmarketcap.com/v1/ticker/',
        params={'convert': 'EUR', 'limit': 1000}
    ).json()

    result = {}
    for d in data:
        sym = d['symbol']
        # data from coinmarketcap seems to be ordered by capitalization descending - we handle tickers by
        # ignoring shitcoins with lower capitalization
        if sym not in result:
          result[sym] = d
    return result


@memo
def get_price(ticker, date=None):
    # cryptocompare is very fragile service. If the (seems to be) global api-rate is reached, it may
    # be helpful to try later: https://www.cryptocompare.com/api/#
    for i in range(10):
        try:
            if date == None:
                return get_current_price_coinmarketcap(ticker)
            return get_historical_price(ticker, date)
        except ApiError:
            time.sleep(i * 3) # sleep up to 30 seconds before attempting the next request
            pass
        except Exception as e:
            raise e
    raise ApiError()

def get_historical_price(ticker, date):
    if type(date) == str:
        date = dateutil.parser.parse(date)

    url = 'https://min-api.cryptocompare.com/data/pricehistorical'
    params = {
        'fsym': ticker,
        'tsyms': 'EUR',
        'ts': int(date.replace(tzinfo=timezone.utc).timestamp()),
        # the total volume to / the total volume from
        'calculationType': 'VolFVolT',
    }

    response = requests.get(url, params=params).json()

    try:
        return response[ticker]['EUR']
    except KeyError:
        raise ApiError()

@memo
def get_current_price_cryptocompare(ticker):
    url = 'https://min-api.cryptocompare.com/data/price'
    params = {'fsym': ticker, 'tsyms': 'EUR'}
    response = requests.get(url, params=params).json()

    try:
        return response['EUR']
    except KeyError:
        print('WARNING: Could not get price for ticker %s, returning 0' % ticker)
        raise ApiError()

def get_current_price_coinmarketcap(ticker):
    return float(currency_info()[ticker]['price_eur'])

if __name__ == '__main__':
    for ticker in ['ETH', 'BTC']:
        # check that both string and datetime work and are consistent
        p1 = get_historical_price(ticker, datetime(2017, 8, 12))
        p2 = get_historical_price(ticker, '2017-08-12')
        assert(p1 == p2)

    # check data correctness (compare two data sources):
    # print all currencies with price difference more than 3%
    from data import currency_constants as c
    ci = currency_info()
    for ticker in c.__all__:
        p1 = float(get_current_price_cryptocompare(ticker))
        p2 = float(get_current_price_coinmarketcap(ticker))
        diff = (p1 - p2) / p2

        if not diff < 0.03:
            print(ticker, diff)
