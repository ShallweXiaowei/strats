# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:40:07 2020

@author: shufe
"""

import pandas as pd
import talib as ta
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm

files = os.listdir('./EOD_data/')

down = pd.DataFrame()
up = pd.DataFrame()
rs = {}
res = pd.DataFrame()
spy = pd.read_csv('./EOD_data/'+'SPY.csv', index_col = 0, parse_dates = True)['2020'].sort_index()
spy.columns = spy.columns.map(lambda x: x.split(' ')[-1])

class stock(object):
    def __init__(self, ticker, df):
        self.ticker = ticker
        self.df = df
        
    def calc_sharpe(self,spy):
        self.df['spy'] = spy['close']
        pct = self.df.pct_change(1)
        pct['ad_ret'] = pct['close'] - pct['spy']
        self.mean = (1+pct['ad_ret'].mean())**252 - 1
        self.std = pct['close'].std()*np.sqrt(252)
        self.sharpe = self.mean/self.std
        X = sm.add_constant(pct['spy'].dropna())
        Y = pct['close'].dropna()
        model = sm.OLS(Y,X).fit()
        self.r2 = model.rsquared
        self.beta = model.params['spy']
        

stocks = []

for file in files:       
    df = pd.read_csv('./EOD_data/'+ file, index_col = 0, parse_dates = True)['2020'].sort_index()
    df.columns = df.columns.map(lambda x: x.split(' ')[-1])
    
    if df['close'].mean() < 5:
        print ('removed %s'%file)
        continue
    
    ticker = file.split('.')[0]
    s = stock(ticker, df)
    s.calc_sharpe(spy)
    stocks.append(s)
    print ('finished %s'%file)

res = {'ticker':[], 'mean':[],'std':[],'sharpe':[],'beta':[],'r2':[]}
for stock in stocks:
    res['ticker'].append(stock.ticker)
    res['mean'].append(stock.mean)
    res['std'].append(stock.std)
    res['sharpe'].append(stock.sharpe)
    res['beta'].append(stock.beta)
    res['r2'].append(stock.r2)
    
    
df = pd.DataFrame(res)
df.to_csv('sharpe.csv')
    
    

