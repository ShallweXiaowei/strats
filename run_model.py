# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 21:16:51 2020

@author: shufe
"""

#from build_model import concat_earning
from download_eod import save_eod
from  multiprocessing import Pool
import pickle
import pandas as pd
from yahoo_real_time import yahoo_quote
from analysis_run import generate_input
from download_intraday import save_intra_eod

#earning = concat_earning(2)
earning = pd.read_csv('earning_all.csv',index_col = 0, parse_dates = True)
ind = earning.index.unique()
earning = earning.loc[ind[:2]]

downs = earning['symbol'].unique()
def quote_list(downs):
    quote_dic = {}
    p = Pool(12)
    for i in downs:
        try:
            #quote_dic[i] = yahoo_quote(i)
            temp = p.apply_async(yahoo_quote,args = (i,))
            quote_dic[i] = temp
            print ('finished quote %s'%i)
        except:
            print('%s error'%i)
    p.close()
    p.join()
    quote_dic = {k:v.get() for k,v in quote_dic.items() if v.successful() }
    quo = pd.DataFrame(quote_dic).transpose()
    quo.columns = ['time','price']
    return quo

def download_intraday_update(downs):
    p = Pool(12)
    for i in downs:
        p.apply_async(save_intra_eod, args = (i,))
        
    p.close()
    p.join()

def download_eod_update(downs):
    p = Pool(12)
    for i in downs:
        p.apply_async(save_eod, args = (i,))
        
    p.close()
    p.join()


def replace(quo):
    for i, row in quo.iterrows():
        ticker = row.name
        df = pd.read_csv('D:/projects/stock/EOD_data/%s.csv'%ticker, index_col = 0, parse_dates = True)
        ins = pd.Series({'open':row['price'],'high':None, 'low':None,'close':None,'volume':None},name = row['time'].date())
        df = df.append(ins)
        df = df.sort_index(ascending = False)
        df.to_csv('D:/projects/stock/EOD_data/%s.csv'%ticker)

def predict():
    with open('best_model_20200726.pkl','rb') as f:
        model = pickle.load(f)
    
    
    df = pd.read_csv('earning_run_price.csv',index_col = 0 ,parse_dates = True)
    #df = df.dropna()
    df = df[df['cap']>5000]
    
    #df['close_ret'] = df['close']/df['before'] - 1
    df['spy_ret'] = df['spy_after']/df['spy_before'] - 1
    df['after'] = df['after']/df['before'] - 1
    df['target'] = df['cons']+df['beta']*df['spy_ret']
    df['alpha'] = df['after'] - df['target']
    df['earn_surp'] = df['Reported_eps'] - df['Estimate_eps']
    df['sales_ratio'] = df['Reported_sales']/df['cap']
    df['sales_surp'] = df['Reported_sales']/df['Estimate_sales'] - 1
    
    df = df[(~df['earn_surp'].isnull()) &(~df['sales_surp'].isnull())]
    
    xcol = ['after', 'alpha', 'macd_before', 'cons', 'spy_ret', 'target',
       'sales_surp', 'earn_surp', 'spy_before', 'spy_after', 'Estimate_eps']
    
    pre = model.predict(df[xcol])
    df['pre'] = pre
    df['pre_target'] = df['before']*(1+df['pre'])
    df['pre_target_low'] = df['before']*(1+df['pre'] - 0.025)
    
    df.to_csv('predict.csv')


if __name__ == '__main__':
    #download_eod_update(downs)
    download_intraday_update(downs)
# =============================================================================
#     quo = quote_list(downs)
#     quo.to_csv('real_time_quote.csv')
#     replace(quo)
#     generate_input(earning)
#     predict()
# =============================================================================
    

