# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 20:51:51 2020

@author: shufe
"""

from build_model import concat_earning, model_ret, get_before_after,get_intra_price
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from multiprocessing import Pool, cpu_count
import os

#earning = concat_earning(-25)
earning = pd.read_csv('earning_all.csv',index_col = 0, parse_dates = True)

def add_prop(row):
    print ('starting task %s'%str(os.getpid()))
    ticker = row['symbol']
    date = row.name.date()
    timing = row['timing']
    try:
        p = pd.Series(get_before_after(ticker,date,timing))
        name = row.name
        row = row.append(p)
        row.name = name
        #intra = get_intra_price(ticker,date,timing)
# =============================================================================
#         row.set_value('before',p[0])
#         row.set_value('after',p[1])
#         row.set_value('close',p[2])
#         row.set_value('spy_before',p[3])
#         row.set_value('spy_after',p[4])
#         row.set_value('cons',p[5])
#         row.set_value('beta',p[6])
#         row.set_value('r2',p[7])
#         row.set_value('dev',p[8])
#         row.set_value('macd_before',p[9])
#         row.set_value('macd_after',p[10])
#         row.set_value('open_2d',p[11])
# =============================================================================
# =============================================================================
#         intra = get_intra_price(ticker,date,timing)
#         row.set_value('t_1000',intra[0])
#         row.set_value('t_1100', intra[0])
#         row.set_value('t_1200', intra[2])
#         row.set_value('t_1300', intra[3])
#         row.set_value('t_1400', intra[4])
#         row.set_value('t_1500', intra[5])
# =============================================================================
        return row
    except:
        return
    
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
    df.to_csv('earning_wt_price.csv')
    
    



# =============================================================================
# for i, row in earning.iterrows():
#     ticker = row['symbol']
#     date = row.name.date()
#     timing = row['timing']
#     try:
#         p = get_before_after(ticker,date,timing)
#         intra = get_intra_price(ticker,date,timing)
#         be, af,cl = p[0],p[1],p[2]
#         before.append(be)
#         after.append(af)
#         close.append(cl)
#         spy_before.append(p[3])
#         spy_after.append(p[4])
#         t_1000.append(intra[0])
#         t_1030.append(intra[1])
#         t_1100.append(intra[2])
#         
#     except:
#         before.append(np.nan)
#         after.append(np.nan)
#         close.append(np.nan)
#         spy_before.append(np.nan)
#         spy_after.append(np.nan)
#         t_1000.append(np.nan)
#         t_1030.append(np.nan)
#         t_1100.append(np.nan)
#     count +=1
#     if count%50 == 0:
#         print ('finished %d'%count)
#         
# earning['before'] = before
# earning['after'] = after
# earning['close_'] = close
# earning['spy_before'] = spy_before
# earning['spy_after'] = spy_after
# 
# earning = earning.dropna()
# earning['ret'] = earning['after']/earning['before'] - 1
# earning['spy_ret'] = earning['spy_after']/earning['spy_before'] - 1
# 
# count = 0
# pre_ret,r2 = [],[]
# for i, row in earning.iterrows():
#     ticker = row['symbol']
#     d = row.name.date()
#     x_input = row['spy_ret']
#     m_ret = model_ret(ticker,x_input,d)
#     pre_ret.append(m_ret[0])
#     r2.append(m_ret[1])
#     count +=1
#     if count%50 == 0:
#         print ('finished %d'%count)
# 
# pre_ret = [x[0] for x in pre_ret]
# earning['pre'] = pre_ret
# earning['r2'] = r2
# earning['adj'] = earning['ret'] - earning['spy_ret']
# 
# 
# 
# 
# 
# 
# 
# =============================================================================










