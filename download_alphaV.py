# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:16:49 2020

@author: shufe
"""
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime

ts = TimeSeries(key='G7CNU4GTGIKJ5SJE',output_format='pandas')
data = ts.get_intraday('GOOGL', outputsize='full')


def get_quote(ticker):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=%s&apikey=%s&datatype=csv'%(ticker,'G7CNU4GTGIKJ5SJE')
    return pd.read_csv(url).iloc[0]


def quote_replace(ticker):
    today = datetime.today()
    df = get_quote(ticker)
    df = pd.DataFrame(df).transpose()[['open','high','low','price','volume']]
    df = df.applymap(float)
    df.index = [today]
    df.index.name = 'date'
    
    odf = pd.read_csv('./EOD_data/%s.csv'%ticker,index_col = 0, parse_dates = True)
    df.columns = odf.columns
    if odf.index[0].date() == today.date():
        odf.loc[today.date().strftime('%Y-%m-%d'),'4. close'] = df['4. close'].iloc[0]
    else:
        odf = pd.concat([df,odf])
    
    odf.to_csv('./EOD_data/%s.csv'%ticker)
    print ('replaced %s on %s'%(ticker, datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
# =============================================================================
# def hist(symbol):
#     symbol = 'AAPL'
#     url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&apikey=%s&datatype=csv&outputsize=full'%(symbol,api_key)
#     df = pd.read_csv(url,index_col = 0,parse_dates = True)
#     return df
# 
# 
# =============================================================================

if __name__ == '__main__':
    quote_replace('AAPL')