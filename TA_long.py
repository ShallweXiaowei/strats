# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 13:28:00 2020

@author: shufe
"""

import pandas as pd
import talib as ta
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
from multiprocessing import Pool, cpu_count, Queue


files = os.listdir('./EOD_data/')

down = pd.DataFrame()
up = pd.DataFrame()
rs = {}
res = pd.DataFrame()
spy = pd.read_csv('./EOD_data/'+'SPY.csv', index_col = 0, parse_dates = True)['2020':'2018'].sort_index()
spy.columns = spy.columns.map(lambda x: x.split(' ')[-1])

#agg_df = pd.DataFrame()
agg_df = []
def process_df(file):
    print ('starting task %s'%str(os.getpid()))
    #file = 'FB.csv'
    try:
        df = pd.read_csv('./EOD_data/'+ file, index_col = 0, parse_dates = True)['2020'].sort_index()
    except:
        return
    df.columns = df.columns.map(lambda x: x.split(' ')[-1])
    ticker = file.split('.')[0]
# =============================================================================
#     if df['close'].mean() < 5:
#         print ('removed %s'%file)
#         return
# =============================================================================
    try:
        macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26, signalperiod=9)
    except:
        return
    df['hist'] = macdhist
    df['macd_long'] = macdsignal
    df['macd_short'] = macd
    
    df['open_hist'] = df.index.map(lambda x: ta.MACD(np.array(list(df.loc[:x]['close'])+[df.loc[x]['open']]), fastperiod=12, slowperiod=26, signalperiod=9)[2][-1])
    
    df['ret_5d'] = df.shift(-5)['close']/df['close'] - 1
    df['ret_3d'] = df.shift(-3)['close']/df['close'] - 1
    df['ret_2d'] = df.shift(-2)['close']/df['close'] - 1
    df['ret_1d'] = df.shift(-1)['close']/df['close'] - 1
    df['ret_10d'] = df.shift(-10)['close']/df['close'] - 1
    df['mom'] = df['hist']/df.std()['hist']
    def crit_1(arr):
        dif = [arr[i] - arr[i-1] for i in range(1,len(arr))]
        if min(arr) > 0 and min(dif[-3:]) > 0 and max(dif[:-3]) < 0:
            return 1
        else:
            return 0
    def crit_2(arr):
        dif = [arr[i] - arr[i-1] for i in range(1,len(arr))]
        if min(arr) > 0 and min(dif[-2:]) > 0 and max(dif[:-2]) < 0:
            return 1
        else:
            return 0
    
    def flop(date,df):
        try:
            op = df.loc[date]['open_hist']
            hi = df.loc[:date]['hist'].iloc[-2]
            if op > 0 and hi < 0:
                return 1
            else:
                return 0
        except:
            return 0
        
    def new_high(date,df):
        op = df.loc[date]['open']
        pre_high = df.loc[:date][-4:-1]['high'].max()
        if op > pre_high:
            return 1
        else:
            return 0
    
    df['ind3'] = df.index.map(lambda x: flop(x,df))
    df['ind4'] = df.index.map(lambda x: new_high(x,df))
        
    df['ind1'] = df['hist'].rolling(8).apply(crit_1, raw = True)
    df['ind2'] = df['hist'].rolling(7).apply(crit_2, raw = True)
    df['final_sig'] = df['ind3'] + df['ind4']
    
    
    sec = df[df['final_sig'] == 2]
    sec['ticker'] = [ticker]*sec.shape[0]
    if sec.empty:
        return
    else:
        return sec
    #globals()['agg_df'] = pd.concat([globals()['agg_df'],sec])
    
if __name__ == '__main__':
    agg_df = []
    p = Pool(15)
    for file in files:
        temp = p.apply_async(process_df,args = (file,))
        agg_df.append(temp)
    p.close()
    p.join()
    agg_df = [x.get() for x in agg_df]
# =============================================================================
#     for file in files:
#         agg_df.append(process_df(file))
# =============================================================================
    agg_df = pd.concat(agg_df)
    agg_df = agg_df.sort_index(ascending = False)
    #print (agg_df)
    des = agg_df.dropna().describe()
    agg_df['ret_2d'].hist(bins = 50)
    sharpe = pd.read_csv('sharpe.csv',index_col = 1).drop(['Unnamed: 0'],axis = 1)
    df = pd.merge(agg_df, sharpe,how = 'left' ,on = ['ticker']).set_index(agg_df.index)
    df.index = df.index.map(lambda x: x.date())
    df.to_csv('res.csv')
    print (des[['ret_2d','ret_1d','ret_3d','ret_5d','ret_10d']])
# =============================================================================
# plt.figure(figsize = (15,7.5))
# plt.subplot(211)
# plt.plot(df['close'])
# plt.subplot(212)
# plt.bar(df.index,df['hist'])
# plt.show()
# =============================================================================




