
api_key = '771f2d51-f922-4595-865c-c8f38d15cb0f'

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
quote_last_url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
matic = 'MATIC'
url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
param_matic = {
    'symbol': matic
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': api_key,
}



def get_matic_price():
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(quote_last_url, params=param_matic)
        data = json.loads(response.text)
        print(data)
        f_usdt_price = data['data']['MATIC'][0]['quote']['USD']['price']
        print(f_usdt_price)
        return {'code': 200,
                'price': f_usdt_price}
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return {'code': 404,
                'msg': e}