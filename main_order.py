#!/usr/bin/python

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from order import Order

ANALYSE_DAYS = 3
API_KEY = 'CoinAPI-API-KEY'

def main():
    date_to = datetime.now()
    date_from = date_to - timedelta(ANALYSE_DAYS)

    url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1HRS&time_start=' + date_from.strftime("%Y-%m-%dT%H:%M:%S") + '&time_end=' + date_to.strftime("%Y-%m-%dT%H:%M:%S") + '&limit=300'
    headers = {'X-CoinAPI-Key' : API_KEY}
    response = requests.get(url, headers=headers)

    try:
        res = json.loads(response.text)
        df = pd.DataFrame.from_dict(res)
        order = Order(df)
        order.make_order()
    except:
        print(response.text)

if __name__ == "__main__":
    main()