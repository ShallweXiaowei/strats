# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:29:06 2019

@author: shufe
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import statsmodels.api as sm
import talib as ta


earning_folder = os.getcwd() + '/earnings/'
files = os.listdir(earning_folder)

eod_folder = os.getcwd()+'/EOD_data/'
spy = pd.read_csv(eod_folder + 'SPY.csv',index_col = 0, parse_dates = True).sort_index()
intra_folder = os.getcwd()+'/intra_day/'

def model_ret(ticker, x_input,date):
    df = pd.read_csv(eod_folder + '%s.csv'%ticker,index_col = 0, parse_dates = True).loc[date:date-timedelta(365)]
    df = df.merge(spy[['open','close']],left_index = True, right_index = True)
    df['ret_spy'] = df['open_y']/df['close_y'].shift(-1) - 1
    df['ret_s'] = df['open_x']/df['close_x'].shift(-1) - 1
    df = df.dropna()
    
    
    x = sm.add_constant(df['ret_spy'])
    y = df['ret_s']
# =============================================================================
#     x = sm.add_constant(df['close_y'])
#     y = df['close_x']
# =============================================================================
    model = sm.OLS(y,x).fit()
    #print(model.summary())
    r2 = model.rsquared
    
    return model.predict([1,x_input]), r2


def get_before_after(ticker, date, timing):
    df = pd.read_csv(eod_folder + '%s.csv'%ticker,index_col = 0, parse_dates = True).sort_index()
    ind = [x.date() for x in df.index]
    ind.index(date)
    if timing == 'amc':
        date = ind[ind.index(date)+1]
    
    date_2 = ind[ind.index(date)+1]
    after = df.loc[:date].iloc[-1]['open']
    close = df.loc[:date].iloc[-1]['close']
    low = df.loc[:date].iloc[-1]['low']
    before = df.loc[:date].iloc[-2]['close']
    vol = df.loc[:date].iloc[-2]['volume']
    spy_before = spy.loc[:date].iloc[-2]['close']
    spy_after = spy.loc[:date].iloc[-1]['open']
    open_2d = df.loc[date_2]['open']
    high_2d = df.loc[date_2]['high']
    
    
    sec = df.loc[:date][-252:]
    mer = sec.merge(spy[['close']],how = 'inner',left_index = True, right_index = True)
    mer = mer.pct_change(-1).dropna()
    model = sm.OLS(mer['close_x'],sm.add_constant(mer['close_y'])).fit()
    sec = sec.iloc[-30:]
    dev = (vol - sec['volume'].mean())/sec['volume'].std()
    
    macd_s = np.array(df.loc[:date].iloc[:-1]['close'])
    #macd, macdsignal, macdhist = ta.MACD(macd_s, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_a,macdsignal_a,macdhist_a = ta.MACD(np.array(list(macd_s)+[df.loc[date]['open']]), fastperiod=12, slowperiod=26, signalperiod=9)
    rsi = ta.RSI(np.array(list(macd_s)+[df.loc[date]['open']]))

    return {'before':before,'after':after,'spy_before':spy_before,'spy_after':spy_after,
            'cons':model.params.iloc[0], 'beta':model.params.iloc[1],'r2':model.rsquared,'dev':dev,
            'macd_before':macdhist_a[-1],'macd_after':macdhist_a[-2],'rsi':rsi[-1],'open_2d':open_2d,
            'macd_2':macdhist_a[-3],'macd_3':macdhist_a[-4],'macd_4':macdhist_a[-5],
            'macd_5':macdhist_a[-6],'macd_6':macdhist_a[-7],'macd_7':macdhist_a[-8]}
# =============================================================================
#     return (before, after,close, spy_before,spy_after,
#             model.params.iloc[0], model.params.iloc[1],model.rsquared,dev, 
#             macdhist_a[-1],macdhist_a[-2],
#             open_2d)
# =============================================================================

def get_before_after_run(ticker, date, timing):
    df = pd.read_csv(eod_folder + '%s.csv'%ticker,index_col = 0, parse_dates = True).sort_index()
    ind = [x.date() for x in df.index]
    ind.index(date)
    if timing == 'amc':
        date = ind[ind.index(date)+1]
    
    #date_2 = ind[ind.index(date)+1]
    after = df.loc[:date].iloc[-1]['open']
    close = df.loc[:date].iloc[-1]['close']
    before = df.loc[:date].iloc[-2]['close']
    vol = df.loc[:date].iloc[-2]['volume']
    spy_before = spy.loc[:date].iloc[-2]['close']
    spy_after = spy.loc[:date].iloc[-1]['open']    
    
    sec = df.loc[:date][-252:]
    mer = sec.merge(spy[['close']],how = 'inner',left_index = True, right_index = True)
    mer = mer.pct_change(-1).dropna()
    model = sm.OLS(mer['close_x'],sm.add_constant(mer['close_y'])).fit()
    sec = sec.iloc[-30:]
    dev = (vol - sec['volume'].mean())/sec['volume'].std()
    
    macd_s = np.array(df.loc[:date].iloc[:-1]['close'])
    #macd, macdsignal, macdhist = ta.MACD(macd_s, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_a,macdsignal_a,macdhist_a = ta.MACD(np.array(list(macd_s)+[df.loc[date]['open']]), fastperiod=12, slowperiod=26, signalperiod=9)

    return (before, after,close, spy_before,spy_after,
            model.params.iloc[0], model.params.iloc[1],model.rsquared,dev, 
            macdhist_a[-1],macdhist_a[-2])

    
def get_intra_price(ticker, date, timing):
    df = pd.read_csv(intra_folder + '%s.csv'%ticker,index_col = 0, parse_dates = True)
    ind = sorted(list(set([x.date() for x in df.index])))
    if timing == 'amc':
        date = ind[ind.index(date)+1]
    
    #prior_sec = df.loc[str(ind[ind.index(date)-1])].sort_index()
    sec = df.loc[str(date)].sort_index()
    t_1000 = sec.loc[str(date)+ ' 10:00']['close']
    #t_1030 = sec.loc[str(date)+ ' 10:30']['close']
    t_1100 = sec.loc[str(date)+ ' 11:00']['close']
    t_1200 = sec.loc[str(date)+ ' 12:00']['close']
    t_1300 = sec.loc[str(date)+ ' 13:00']['close']
    t_1400 = sec.loc[str(date)+ ' 14:00']['close']
    t_1500 = sec.loc[str(date)+ ' 15:00']['close']
    
    return t_1000,t_1100,t_1200,t_1300,t_1400,t_1500
    
    
def clean_cap(x):
    if str(x) == 'nan':
        return np.nan
    else:
        return int(str(x).replace(',','').split('.')[0])
def clean_est(x):
    if str(x) == '--':
        return np.nan
    else:
        return float(str(x).replace(',',''))
    
    
def concat_earning(n):
    res = pd.DataFrame()
    for i in files[-n:]:
        date = datetime.strptime(i.split('.')[0],'%Y%m%d')
        df = pd.read_csv(earning_folder + i,index_col = 0, parse_dates = True)
        df.index = [date]*df.shape[0]
        res = pd.concat([res,df])
        
    res['cap'] = res['cap'].map(lambda x: clean_cap(x))
    res = res[res['timing'].isin(['amc','bmo'])]
    res['est'] = res['est'].map(lambda x: clean_est(x))
    res['report'] = res['report'].map(lambda x: clean_est(x))
    res['surp'] = res['report'] - res['est']
    res['pct_surp'] = res['report']/res['est'] - 1
    res = res.sort_index(ascending = False)
    return res


if __name__ == '__main__':
    df = concat_earning(30)


















