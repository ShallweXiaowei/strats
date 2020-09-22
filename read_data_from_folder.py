# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 14:13:39 2020

@author: shufe
"""

import pandas as pd
import os


files = os.listdir('./EOD_data/')

down = pd.DataFrame()
up = pd.DataFrame()
for file in files:
    df = pd.read_csv('./EOD_data/'+file, index_col = 0, parse_dates = True)['2020']
    df.columns = df.columns.map(lambda x: x.split(' ')[-1])
    df['last_low'] = df.shift(-1)['low']
    df['high/last_low'] = df['high']/df['last_low'] - 1
    df['last_high'] = df.shift(-1)['high']
    df['low/last_high'] = df['low']/df['last_low'] - 1
    df['ret_next_day'] = df.shift(1)['open']/df['close'] - 1
    df['ret_next_day_end'] = df.shift(1)['close']/df['close'] - 1
    
    down_df = df[df['high/last_low'] < -0.03]
    up_df = df[df['low/last_high'] > -0.03]
    
    if down_df.shape[0] > 0:
        ticker = file.split('.')[0]
        down_df['ticker'] = ticker
        down = pd.concat([down,down_df],axis = 0)
    
    if up_df.shape[0] > 0:
        ticker = file.split('.')[0]
        up_df['ticker'] = ticker
        up = pd.concat([up,up_df],axis = 0)  
    
    print ('append %s'%file)


down = down.sort_index(ascending = False)
down.describe()

sec = down[(down['high/last_low'] < -0.06) & (down['high/last_low'] > -0.2) & (down['close'] < down['open'])]
sec.describe()

sec['ret_next_day'].plot.hist()
sec['ret_next_day_end'].plot.hist()
