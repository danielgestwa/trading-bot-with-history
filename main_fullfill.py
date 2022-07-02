#!/usr/bin/python

import json
from datetime import datetime
from fullfill_orders import Fullfill
from requests import Session

API_KEY = 'CMC-API-KEY'

def main():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'limit':'1'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    price = data['data'][0]['quote']['USD']['price']

    str_now = datetime.now()

    ff = Fullfill(price, str_now)
    ff.check_fullfill_order()

if __name__ == "__main__":
    main()