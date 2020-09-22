# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:27:12 2020

@author: shufe
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from  multiprocessing import Pool
import os
import time
import sys


l = list(pd.read_excel('sp500list.xlsx')['Symbol'])
ts = TimeSeries(key='G7CNU4GTGIKJ5SJE',output_format='pandas')
rus = list(pd.read_csv('russell-1000-index-04-12-2020.csv')['Symbol'])[:-1]
rus_2000 = list(pd.read_excel('rus_2000.xlsx',header = None).iloc[:,0])
earn = pd.read_csv('earning_list.csv')['symbol'].unique()
etf = list(pd.read_csv('etf_sector_list.csv')['ticker'])
intl = list(pd.read_csv('int_list.csv')['Ticker'])

def get_end(ticker):
    api_key = 'G7CNU4GTGIKJ5SJE'
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=%s&interval=5min&outputsize=full&apikey=%s&datatype=csv'%(ticker,api_key)
    df = pd.read_csv(url,index_col = 0, parse_dates = True)
    return df

def quote(ticker):
    api_key = 'G7CNU4GTGIKJ5SJE'
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s&datatype=csv'%(ticker, api_key)
    df = pd.read_csv(url)
    return df


def save_intra_eod(ticker, path = './intra_day/'):
    print('Run task %s (%s)...' % (ticker, os.getpid()))
    start = time.time()
    try:
        data = get_end(ticker)
        data.to_csv(path + ticker +'.csv')
    except:
        print ('%s'%sys.exc_info()[0])
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (ticker, (end - start)))
    time.sleep(2)

if __name__ == '__main__':
    p = Pool(12)
    for i in intl:
        p.apply_async(save_intra_eod, args = (i,))

    p.close()
    p.join()
