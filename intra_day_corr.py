# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:20:42 2020

@author: shufe
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm

int_path = './intra_day/'
eod_path = './EOD_data/'
l = list(pd.read_csv('int_list.csv')['Ticker'])


df_dic = {}
for t in l:
    d = pd.read_csv(int_path + t + '.csv', index_col = 0, parse_dates = True).sort_index()
    df_dic[t] = d
    
eod_df = {}
for t in l:
    d = pd.read_csv(eod_path + t + '.csv', index_col = 0, parse_dates = True).sort_index()
    eod_df[t] = d

param_dic = {}
for k in df_dic.keys():
    df = pd.concat([eod_df['QQQ']['close'], eod_df[k]['close']],axis = 1).dropna()['2019':].pct_change().dropna()
    x = sm.add_constant(df.iloc[:,0])
    y = df.iloc[:,1]
    mod = sm.OLS(y,x).fit()
    param_dic[k] = mod.params


def corr_qqq(ticker):
    qqq = df_dic['QQQ']
    dates = sorted(list(set([x.date() for x in qqq.index])))
    d = df_dic[ticker]
    cor_dic = {}
    for date in dates:
        df = pd.concat([d['close'][str(date)],qqq['close'][str(date)]],axis = 1).between_time('9:30','16:00')
        cor_dic[date] = df.corr().iloc[0].iloc[1]
        
    return pd.Series(cor_dic,name = ticker).sort_index()

df = pd.DataFrame()
for k in df_dic.keys():
    if k not in ['SPY','QQQ']:
        s = corr_qqq(k)
        df = pd.concat([df,s],axis = 1,sort=True)

def check(ticker):
    df = pd.concat([eod_df['QQQ']['close'],eod_df[ticker]['close']],axis = 1).pct_change().dropna()
    df.columns = ['QQQ',ticker]
    df['exp_ret'] = df['QQQ']*param_dic[ticker].iloc[1] + param_dic[ticker].iloc[0]
    df['alpha'] = df[ticker] - df['exp_ret']
    cor = corr_qqq(ticker).rename('corr')
    df = pd.concat([df,cor],axis = 1)
    return df



if __name__ == '__main__':
    c = check('NVDA')
    
    
    
    
    
    
    
    