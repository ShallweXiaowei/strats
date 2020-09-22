# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:11:21 2020

@author: shufe
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from  multiprocessing import Pool
import os
import time
from download_alphaV import quote_replace

l = list(pd.read_excel('sp500list.xlsx')['Symbol'])
ts = TimeSeries(key='G7CNU4GTGIKJ5SJE',output_format='pandas')
rus = list(pd.read_csv('russell-1000-index-04-12-2020.csv')['Symbol'])[:-1]
rus_2000 = list(pd.read_excel('rus_2000.xlsx',header = None).iloc[:,0])




def save_eod(ticker, path = './real_time/'):
    print('Run task %s (%s)...' % (ticker, os.getpid()))
    start = time.time()
    try:
        quote_replace(ticker)
    except:
        return
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (ticker, (end - start)))
    time.sleep(2)
    
if __name__ == '__main__':
    p = Pool(16)
    for i in rus:
        p.apply_async(save_eod, args = (i,))
    
    p.close()
    p.join()
    
        