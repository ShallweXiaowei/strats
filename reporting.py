# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:18:00 2020

@author: shufe
"""

import pandas as pd
from yahoo_real_time import yahoo_quote
from run_model import quote_list
import numpy as np
import time

df = pd.read_csv('predict.csv',index_col = 0, parse_dates = True)

rep = df[['symbol','Company','pre','pre_target','pre_target_low']]

if __name__ == '__main__':
    quo = quote_list(df['symbol'])
    rep = rep[rep['symbol'].isin(list(quo.index))]
    rep.loc[:,'now'] = rep['symbol'].map(lambda x: quo.to_dict()['price'][x])
    rep['below'] = np.where(rep['now'] < rep['pre_target_low'], 1,0)
    rep = rep.sort_values(['pre'],ascending = False)
    print (rep)
    while True:
        time.sleep(60)
        try:
            rep.loc[:,'past'] = rep['now']
            rep.loc[:,'old_below'] = rep['below']
            quo = quote_list(rep['symbol'])
            rep.loc[:,'now'] = rep['symbol'].map(lambda x: quo.to_dict()['price'][x])
            rep['below'] = np.where(rep['now'] < rep['pre_target_low'], 1,0)
            print(rep)
            
            
        except:
            print ('error')
        
    