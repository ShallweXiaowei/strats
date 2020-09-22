# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:42:25 2020

@author: shufe
"""

import pandas as pd
import numpy as np



import pandas as pd
import os
from multiprocessing import Pool
import talib as ta
from datetime import datetime

df = pd.read_csv('universe.csv', index_col = 0)
uni = df.index.map(lambda x: x.split(' ')[0])

eod_path = 'D:/projects/stock/EOD_data/'
files = os.listdir(eod_path)

def extract(ticker):
    try:
        d = pd.read_csv(eod_path + ticker +'.csv', index_col = 0 ,parse_dates = True).sort_index()
        ret = d['close'].pct_change()
        ret_intra = d['close']/d['open'] - 1
        jump = d['open']/d.shift()['close']
        return ticker, ret, ret_intra,jump 
    except:
        return



if __name__ == '__main__':
    res = []
    p = Pool(15)
    for file in files:
        ticker = file[:-4]
        temp = p.apply_async(extract, args = (ticker,))
        res.append(temp)
    
    p.close()
    p.join()
    res = [x.get() for x in res]
    res = [x for x in res if x != None]
    dic = {}
    intra_dic = {}
    jump_dic = {}
    for i in res:
        ticker = i[0]
        ret = i[1]
        ret_intra = i[2]
        jump_dic = i[3]
        dic[ticker] = ret
        intra_dic[ticker] = ret_intra
    
    dates = intra_dic['AAPL']['2020'].index
    intra_worst = {}
    for date in dates:
        intra_worst[date] = []
        for k,v in intra_dic.items():
            if date in v.index:
                intra_worst[date].append((k,v[date]))
            else:
                continue
        
        intra_worst[date] = sorted(intra_worst[date], key = lambda x: x[1])
        
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    