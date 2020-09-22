# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 23:31:42 2020

@author: shufe
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 20:51:51 2020

@author: shufe
"""

from build_model import concat_earning, model_ret, get_before_after_run,get_intra_price
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Pool, cpu_count
import os

#earning = concat_earning(3)
earning = pd.read_csv('earning_all.csv',index_col = 0, parse_dates = True)
ind = earning.index.unique()
earning = earning.loc[ind[:2]]


def add_prop(row):
    print ('starting task %s'%str(os.getpid()))
    ticker = row['symbol']
    date = row.name.date()
    timing = row['timing']
    try:
        p = get_before_after_run(ticker,date,timing)
        #intra = get_intra_price(ticker,date,timing)
        row.set_value('before',p[0])
        row.set_value('after',p[1])
        row.set_value('close',p[2])
        row.set_value('spy_before',p[3])
        row.set_value('spy_after',p[4])
        row.set_value('cons',p[5])
        row.set_value('beta',p[6])
        row.set_value('r2',p[7])
        row.set_value('dev',p[8])
        row.set_value('macd_before',p[9])
        row.set_value('macd_after',p[10])
        #row.set_value('open_2d',p[11])
        return row
    except:
        return

def generate_input(earning):
    agg_df = []
    p = Pool(15)
    for i, row in earning.iterrows():
        temp = p.apply_async(add_prop,args = (row,))
        agg_df.append(temp)
    p.close()
    p.join()
    agg_df = [x.get() for x in agg_df]
    agg_df = [x for x in agg_df if type(x) != type(None)]
    df = pd.DataFrame(agg_df)
    df = df.sort_index(ascending = False)
    df.to_csv('earning_run_price.csv')
    
if __name__ == '__main__':
    agg_df = []
    p = Pool(15)
    for i, row in earning.iterrows():
        temp = p.apply_async(add_prop,args = (row,))
        agg_df.append(temp)
    p.close()
    p.join()
    agg_df = [x.get() for x in agg_df]
    agg_df = [x for x in agg_df if type(x) != type(None)]
    df = pd.DataFrame(agg_df)
    df = df.sort_index(ascending = False)
    df.to_csv('earning_run_price.csv')
    








