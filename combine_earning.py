# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:25:26 2020

@author: shufe
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

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
    
path = 'D:/projects/stock/earning_raw/'
files = os.listdir(path)
dates = list(set([x.split('_')[1].split('.')[0] for x in files]))

df = pd.DataFrame()
for date in dates:
    df1 = pd.read_csv(path+ 'earns_'+date+'.csv', index_col = 0)
    df2 = pd.read_csv(path+ 'sales_'+date+'.csv',index_col = 0)
    m = pd.merge(df1,df2[['Estimate','Reported']],left_index = True, right_index = True,suffixes = ('_eps','_sales'))
    if m.empty:
        continue
    
    m = m.rename({'Market Cap(M)':'cap','Time':'timing'},axis = 1)
    m['cap'] = m['cap'].map(lambda x: clean_cap(x))
    m = m[m['timing'].isin(['amc','bmo'])]
    for c in ['Estimate_eps', 'Reported_eps','Estimate_sales','Reported_sales']:
        m[c] = m[c].map(clean_est)
    
    m['symbol'] = m.index
    m.index = [datetime.strptime(date,'%Y-%m-%d')]*m.shape[0]
    df = pd.concat([df,m],axis = 0)

df = df.sort_index(ascending = False)
df = df.drop(['%Surp','Price Change','Report','Surprise'],axis = 1)
df.to_csv('earning_all.csv')