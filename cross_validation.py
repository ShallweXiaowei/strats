# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 23:09:55 2020

@author: shufe
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.naive_bayes import GaussianNB
import pickle
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import export_text
from sklearn import svm
from sklearn.datasets import load_boston
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import VotingRegressor
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
import statsmodels.api as sm
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import time


s = time.time()



df = pd.read_csv('earning_wt_price.csv',index_col = 0 ,parse_dates = True)
df = df.drop(['ESP'],axis = 1)
df = df.dropna()
df = df[df['cap']>5000]
df['open_2d'] = df['open_2d'].map(float)
#df = df.loc['2020']

df['timing'] = np.where(df['timing'] =='bmo',0,1)
#df['close_ret'] = df['close']/df['before'] - 1
df['spy_ret'] = df['spy_after']/df['spy_before'] - 1
df['after'] = df['after']/df['before'] - 1
df['target'] = df['cons']+df['beta']*df['spy_ret']
df['alpha'] = df['after'] - df['target']
df['earn_surp'] = df['Reported_eps'] - df['Estimate_eps']
df['sales_ratio'] = df['Reported_sales']/df['cap']
df['sales_surp'] = df['Reported_sales']/df['Estimate_sales'] - 1
df['open_ret'] = df['open_2d']/df['before'] - 1

df = df[(df['open_ret'] < np.percentile(df['open_ret'],99)) & (df['open_ret'] > np.percentile(df['open_ret'],1))]


corr = df.corr()
corr['open_ret'].abs().sort_values(ascending = False)




xcol = corr['open_ret'].abs().sort_values(ascending = False).index[1:]
#xcol = ['after', 'alpha','spy_ret','target','macd_before','cons','spy_before','spy_after','earn_surp','sales_surp']
# =============================================================================
# xcol = ['after', 'alpha', 'before', 'macd_before', 'macd_after',
#        'cons', 'Reported_eps', 'Estimate_eps', 'target', 'beta',
#        'r2']
# =============================================================================

X = df[xcol]
y = df['open_ret']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33)

x_scaler = StandardScaler().fit(X_train)
X_train = x_scaler.transform(X_train)
X_test = x_scaler.transform(X_test)

y_scaler = StandardScaler().fit(y_train.to_numpy().reshape(-1,1))
y_train = y_scaler.transform(y_train.to_numpy().reshape(-1,1))
y_test = y_scaler.transform(y_test.to_numpy().reshape(-1,1))


##########
lin = sm.OLS(pd.DataFrame([x[0] for x in y_train]),sm.add_constant(pd.DataFrame(X_train, columns = xcol))).fit()
lin.summary()
##########

from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
from tensorflow.keras import regularizers
# =============================================================================
# tf.test.is_built_with_cuda()
# tf.test.is_gpu_available(cuda_only=False, min_cuda_compute_capability=None)
# 
# =============================================================================

my_callback = [tf.keras.callbacks.EarlyStopping(patience = 10,restore_best_weights = True),
        ]

model = Sequential()
model.add(Dense(X_train.shape[1], activation = 'relu',input_shape = [X_train.shape[1],]))
model.add(Dense(1024, activation='relu',kernel_regularizer='l2',bias_regularizer=regularizers.l2(0.01)))
model.add(Dense(2048, activation='relu',kernel_regularizer='l1',bias_regularizer=regularizers.l2(0.01)))
model.add(Dense(1024, activation='relu',kernel_regularizer='l2'))
model.add(Dense(1))
model.compile(loss = tf.keras.losses.MeanSquaredError(),optimizer = 'sgd',
              metrics=[tf.keras.metrics.MeanAbsoluteError()])

model.fit(X_train, y_train,validation_split=0.3 ,epochs=1200,
          callbacks = my_callback,
          batch_size = 300, use_multiprocessing = True)

model.evaluate(X_train,y_train)


Y_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)


df['pred'] = y_scaler.inverse_transform(model.predict(x_scaler.transform(df[xcol])))
df['resid'] = (df['pred'] - df['open_ret'])
print(df['resid'].describe())
print(df['resid'].abs().describe())
df.to_csv('validation.csv')


print('using %s'%str(time.time() - s))

plt.figure(figsize = (10,10))
plt.scatter(y_scaler.inverse_transform(y_train_pred),y_scaler.inverse_transform(y_train),c = 'green')
plt.scatter(y_scaler.inverse_transform(Y_pred),y_scaler.inverse_transform(y_test),c = 'blue')
plt.plot(y_scaler.inverse_transform(y_test),y_scaler.inverse_transform(y_test),color = 'r')
plt.show()

# =============================================================================
# with open('best_model_20200726.pkl','wb') as f:
#     pickle.dump(est,f)
# 
# =============================================================================

