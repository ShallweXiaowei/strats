# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 22:18:44 2020

@author: shufe
"""

import pandas as pd
from multiprocessing import Pool
eod_path = './EOD_data/'

uni = pd.read_excel('universe.xlsx',0,index_col = 0)

def get_ret(ticker):
    try:
        sec = pd.read_csv(eod_path + ticker + '.csv',index_col = 0, parse_dates = True).sort_index()
        ret = sec.loc['2020-07-31']['close']/sec.loc['2020-03-23']['close'] - 1
        return ticker, ret
    except:
        return



if __name__ == '__main__':
    p = Pool(15)
    res = []
    for i,row in uni.iterrows():
        ticker = row.name.split(' ')[0]
        temp = p.apply_async(get_ret, args = (ticker,))
        res.append(temp)
        
    res = [x.get() for x in res]
    res = [x for x in res if x != None]
    res = {x[0]:x[1] for x in res}
    df = pd.Series(res)
    df.to_csv('ret_from_march.csv')
        
        