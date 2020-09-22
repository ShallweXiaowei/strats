# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 21:32:49 2020

@author: shufe
"""

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

files = os.listdir('./EOD_data/')

down = pd.DataFrame()
up = pd.DataFrame()
rs = {}
res = pd.DataFrame()
spy = pd.read_csv('./EOD_data/'+'SPY.csv', index_col = 0, parse_dates = True)['2020':'2018'].sort_index()
spy.columns = spy.columns.map(lambda x: x.split(' ')[-1])

agg_df = pd.DataFrame()
for file in files:
    #file = 'FB.csv'
    df = pd.read_csv('./EOD_data/'+ file, index_col = 0, parse_dates = True)['2020'].sort_index()
    df.columns = df.columns.map(lambda x: x.split(' ')[-1])
    
    if df['close'].mean() < 5:
        print ('removed %s'%file)
        continue
    
    macd, macdsignal, macdhist = ta.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['hist'] = macdhist
    df['macd_long'] = macdsignal
    df['macd_short'] = macd
    
    df['ret_5d'] = df.shift(-5)['close']/df['close'] - 1
    df['ret_3d'] = df.shift(-3)['close']/df['close'] - 1
    df['ret_2d'] = df.shift(-2)['close']/df['close'] - 1
    df['ret_1d'] = df.shift(-1)['close']/df['close'] - 1
    df['ret_10d'] = df.shift(-10)['close']/df['close'] - 1
    def crit_1(arr):
        dif = [arr[i] - arr[i-1] for i in range(1,len(arr))]
        if max(dif) < 0 and min(arr) > 0:
            return 1
        else:
            return 0
    df['ind1'] = df['hist'].rolling(4).apply(crit_1, raw = True)
    df['ind2'] = np.where((df['macd_short'] > df['macd_long']) & (df['macd_long'] > df['hist']),1,0)
    
# =============================================================================
    thres = df.std()['hist']*0.2
    df['ind3'] = df['hist'].map(lambda x: 1 if (abs(x) < thres) else 0)
    df['final_sig'] = df['ind1'] + df['ind2'] + df['ind3']
    sec = df[df['final_sig'] == 3] 
    agg_df = pd.concat([agg_df,sec])
    

        
    #print ('finished %s'%file)

des = agg_df.describe()
agg_df['ret_2d'].hist(bins = 50)
print (des['ret_2d'])

# =============================================================================
# plt.figure(figsize = (15,7.5))
# plt.subplot(211)
# plt.plot(df['close'])
# plt.subplot(212)
# plt.bar(df.index,df['hist'])
# plt.show()
# =============================================================================
