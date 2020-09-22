# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 22:03:25 2020

@author: shufe
"""
import pandas as pd
import os
from multiprocessing import Pool
import talib as ta
from datetime import datetime

df = pd.read_csv('universe.csv', index_col = 0)
uni = df.index.map(lambda x: x.split(' ')[0])

eod_path = 'D:/projects/stock/EOD_data/'
files = os.listdir(eod_path)

d = pd.read_csv(eod_path + 'NIO.csv', index_col = 0 ,parse_dates = True).sort_index()

# =============================================================================
# d['ret'] = d['close'].pct_change(-1)
# d['ret_5d'] = d['close'].pct_change(-5)
# 
# d['ret_5d'].plot()
# =============================================================================


def get_ret(ticker,date):  
    try:
        d = pd.read_csv(eod_path + ticker + '.csv', index_col = 0 ,parse_dates = True).sort_index()
        row = d.loc['2020-01-02']
        d = d/row
        
        res = []
        for date in d['2020-02-13':].index:
            try:
                x = d.loc[:date]
                x.loc[:,'macd'], x.loc[:,'macdsignal'], x.loc[:,'macdhist'] = ta.MACD(x['close'], fastperiod=12, slowperiod=26, signalperiod=9)
                x.loc[:,'rsi'] = ta.RSI(x['close'])
                x = x.iloc[:,3:]
                x = x.iloc[-7:]
                x = x.sort_index(ascending = False)
                y = d[date:].iloc[:4].pct_change(3)['open'].iloc[-1]
                res.append(list(x.stack())+[y])
            except:
                continue
        
        return res
    except:
        return



def p_ret():
    p = Pool(16)
    temps = []
    date = datetime(2020,8,20).date()
    for file in files[0]:
        ticker = file.split('.')[0]
        temp = p.apply_async(get_ret,args = (ticker,date,))
        temps.append(temp)
    
    p.close()
    p.join()
    
    temps = [x.get() for x in temps]
    temps = [x for x in temps if x != None]
    res = []
    for i in temps:
        for j in i:
            res.append(j)
    return res

if __name__ == '__main__':
    res = p_ret()
    data = pd.DataFrame(res)
    data.to_csv('train_data.csv')
    
    
    
    
