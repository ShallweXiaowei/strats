# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:18:20 2020

@author: shufe
"""

import pandas as pd
import os
import statsmodels.api as sm
import matplotlib.pyplot as plt

files = os.listdir('./EOD_data/')

down = pd.DataFrame()
up = pd.DataFrame()
rs = {}
res = pd.DataFrame()
spy = pd.read_csv('./EOD_data/'+'SPY.csv', index_col = 0, parse_dates = True)['2020']
spy.columns = spy.columns.map(lambda x: x.split(' ')[-1])

for file in files:
    name = file.split('.')[0]
    df = pd.read_csv('./EOD_data/'+file, index_col = 0, parse_dates = True)['2020']
    df.columns = df.columns.map(lambda x: x.split(' ')[-1])
    df['ret_next_day'] = df.shift(1)['open']/df['close'] - 1
    df['ret_next_day_end'] = df.shift(1)['close']/df['close'] - 1
    df['intra_day_change'] = df['close']/df['open'] - 1
    df['last_intra_change'] = df.shift(-1)['close']/df.shift(-1)['open']
    df['ret'] = df['close']/df.shift(-1)['close'] - 1
    df['low/last_high'] = df['low']/df.shift(-1)['high'] - 1
    df['high/last_low'] = df['high']/df.shift(-1)['low'] - 1
    std = df.std()['ret']


    spy['ret_next_day'] = spy.shift(1)['open']/spy['close'] - 1
    spy['ret_next_day_end'] = spy.shift(1)['close']/spy['close'] - 1
    spy['intra_day_change'] = spy['close']/spy['open'] - 1
    spy['last_intra_change'] = spy.shift(-1)['close']/spy.shift(-1)['open']
    spy['ret'] = spy['close']/spy.shift(-1)['close'] - 1
    spy['low/last_high'] = spy['low']/spy.shift(-1)['high'] - 1
    spy['high/last_low'] = spy['high']/spy.shift(-1)['low'] - 1
    
    df['intra_day_change_spy'] = spy['intra_day_change']
    df['last_intra_change_spy'] = spy['last_intra_change']
    #X = df[['intra_day_change','last_intra_change','intra_day_change_spy','last_intra_change_spy']].dropna().iloc[1:]
    X = df[['last_intra_change','ret','last_intra_change_spy']].dropna().iloc[1:]
    X = sm.add_constant(X)
    Y = df['ret_next_day'].iloc[:-1].dropna()
    model = sm.OLS(Y,X).fit()
    model.summary()
    rs[name] = model.rsquared
    df['predict'] = model.predict(X)
    if model.rsquared > 0.15:
        sec = df[df['predict'] > 0.03]
        #sec = df
        sec['Ticker'] = [name]*sec.shape[0]
        res = pd.concat([res,sec],axis = 0)
        print ('finished %s'%name)
        
res = res.sort_index(ascending = False)
res = res[(res['predict'] < 0.7) & (res['ret_next_day'] < 0.8)]
plt.scatter(res['predict'], res['ret_next_day'])
# =============================================================================
# plt.scatter(model.predict(X), Y)
# =============================================================================
#res = pd.Series(rs)

