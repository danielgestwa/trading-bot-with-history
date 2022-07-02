#!/usr/bin/python

from database import Database
import requests
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta

QUARTILE_DIVIDER = 2
CANCEL_TIME = 5 # [days]
GAIN_PERCENTAGE = 10 # [%]

class Order:
    def __init__(self, df):
        self.db = Database()
        self.df = df
    
    def make_order(self):
        my_df = self.df[['rate_open', 'rate_close', 'rate_high', 'rate_low']]

        mean_median = my_df.median().mean()
        mean_last = my_df.iloc[-1].mean()
        max_rate_heigh = my_df["rate_high"].max()
        min_rate_low = my_df["rate_low"].min()

        quartile = (max_rate_heigh - min_rate_low) / 4
        high_bar = min_rate_low + (quartile * 3)
        middle_bar = min_rate_low + (quartile * 2)
        low_bar = min_rate_low + (quartile)

        margin_type = 'SKIP'
        buy_price = 0
        sell_price = 0
        cancel_price = 0
        stop_loose = 0
        cancel_time = datetime.now()

        if(mean_last * (high_bar - low_bar) / 100 > GAIN_PERCENTAGE):
            direction = 'UP' if mean_median > mean_last else 'DOWN'
            margin = 'LONG' if max_rate_heigh - mean_last > mean_last - min_rate_low else 'SHORT'
            
            if(margin == 'LONG' and direction == 'UP'):
                margin_type = 'LONG'
                buy_price = low_bar - (quartile / QUARTILE_DIVIDER)
                sell_price = high_bar + (quartile / QUARTILE_DIVIDER)
                cancel_price = middle_bar + (quartile / QUARTILE_DIVIDER)
                stop_loose = min_rate_low - (quartile / QUARTILE_DIVIDER)
                cancel_time += timedelta(days=CANCEL_TIME)
                gain = sell_price - buy_price
                loose = buy_price - stop_loose

            if(margin == 'SHORT' and direction == 'DOWN'):
                margin_type = 'SHORT'
                buy_price = high_bar + (quartile / QUARTILE_DIVIDER)
                sell_price = low_bar - (quartile / QUARTILE_DIVIDER)
                cancel_price = middle_bar - (quartile / QUARTILE_DIVIDER)
                stop_loose = max_rate_heigh + (quartile / QUARTILE_DIVIDER)
                cancel_time += timedelta(days=CANCEL_TIME)
                gain = buy_price - sell_price
                loose = stop_loose - buy_price

            if margin_type != 'SKIP':
                gain_loose_div = gain / loose

                self.db.db_open()
                self.db.db_execute_data(
                    'INSERT INTO orders VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)',
                    (margin_type, mean_last, buy_price, sell_price, stop_loose, cancel_price, cancel_time, gain, loose, gain_loose_div)
                )
                self.db.db_close()