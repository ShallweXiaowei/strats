# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 12:49:53 2020

@author: shufe
"""

from datetime import datetime
import pandas as pd

import json, urllib.request
def real_time(symbol):
    res = urllib.request.urlopen('https://cloud.iexapis.com/stable/stock/%s/book?token=pk_6ac472d18510450ba6e71e845f85644c'%symbol)
    js = json.loads(res.read().decode())
    df = pd.DataFrame(js['trades'])
    df['timestamp'] = df['timestamp'].map(lambda x: datetime.fromtimestamp(x/1000))
    df.index = df['timestamp']
    df = df[['price', 'size']]
    return df
def intra_day(symbol):
    intra = 'https://cloud.iexapis.com/stable/stock/%s/intraday-prices?token=pk_6ac472d18510450ba6e71e845f85644c'%symbol
    res = urllib.request.urlopen(intra)
    js = json.loads(res.read().decode())
    df = pd.DataFrame(js)
    df.index = (df['date']+'-'+df['minute']).map(lambda x: datetime.strptime(x, '%Y-%m-%d-%H:%M'))
    df = df.drop(['date','minute','label'],axis = 1)
    df = df.sort_index(ascending = False)
    return df
def hist(symbol):
    url = 'https://cloud.iexapis.com/stable/stock/%s/chart/2y?token=pk_6ac472d18510450ba6e71e845f85644c'%symbol
    res = urllib.request.urlopen(url)
    js = json.loads(res.read().decode())
    df = pd.DataFrame(js)
    df.index = df['date'].map(lambda x: datetime.strptime(x, '%Y-%m-%d'))
    df = df.drop(['date'],axis = 1)
    df = df.sort_index(ascending = False)
    return df


if __name__ == '__main__':
    df = real_time('AAPL')