# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 15:36:18 2020

@author: shufe
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras import optimizers
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
import matplotlib.pyplot as plt
import time
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

def y_trans(y):
    sec = [0,0.025,0.05,0.1]
    for i in range(len(sec)):
        if sec[i] >= y:
            return i
    return len(sec)+1
    
def cate(x):
    x = list(x)
    return x.index(max(x))

s = time.time()

data = pd.read_csv('train_data.csv',index_col = 0)
data = data.replace([np.inf, -np.inf], np.nan)
data = data.dropna()

data = data[(data.iloc[:,-1] < np.percentile(data.iloc[:,-1],99.96)) & (data.iloc[:,-1] < np.percentile(data.iloc[:,-1],99.96))]
data.iloc[:,-1] = data.iloc[:,-1].map(y_trans)

x = data.iloc[:,:-1]
y = data.iloc[:,-1]

encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)
y = np_utils.to_categorical(encoded_Y)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.33)

x_scaler = StandardScaler().fit(X_train)
X_train = x_scaler.transform(X_train)
X_test = x_scaler.transform(X_test)

# =============================================================================
# y_scaler = StandardScaler().fit(y_train.to_numpy().reshape(-1,1))
# y_train = y_scaler.transform(y_train.to_numpy().reshape(-1,1))
# y_test = y_scaler.transform(y_test.to_numpy().reshape(-1,1))
# 
# 
# =============================================================================
my_callback = [tf.keras.callbacks.EarlyStopping(patience = 5),]

model = Sequential()
model.add(Dense(X_train.shape[1], activation = 'softmax',input_shape = [X_train.shape[1],]))
model.add(Dense(1024, activation='relu', kernel_regularizer='l1', bias_regularizer='l2'))
model.add(Dense(512,activation = 'relu', kernel_regularizer='l1', bias_regularizer='l1'))
model.add(Dense(y.shape[1],activation = 'softmax'))

#opt = optimizers.SGD(lr=0.01, momentum=0.9)

model.compile(loss = 'binary_crossentropy',optimizer = 'adam',
              metrics=['accuracy'])

model.fit(X_train, y_train,validation_split=0.3 ,epochs=100,
          callbacks = my_callback,
          batch_size = 100, use_multiprocessing = True)

#model.evaluate(X_train,y_train)


y_train_pred = model.predict(X_train)
y_train_pred = [cate(x) for x in y_train_pred]
print(confusion_matrix([cate(x) for x in y_train],y_train_pred))

Y_pred = model.predict(X_test)
Y_pred = [cate(x) for x in Y_pred]
print(confusion_matrix([cate(x) for x in y_test],Y_pred))



# =============================================================================
# y_train_pred = model.predict(X_train)
# Y_pred = model.predict(X_test)
# 
# plt.scatter(y_scaler.inverse_transform(y_train),y_scaler.inverse_transform(y_train_pred),c = 'green')
# plt.scatter(y_scaler.inverse_transform(y_test),y_scaler.inverse_transform(Y_pred),c = 'blue')
# plt.plot(y_scaler.inverse_transform(y_test),y_scaler.inverse_transform(y_test),color = 'r')
# plt.show()
# =============================================================================

# =============================================================================
# data['pred'] = y_scaler.inverse_transform(model.predict(x_scaler.transform(x)))
# data['resid'] = (data['pred'] - data.iloc[:,-1])
# print(data['resid'].describe())
# print(data['resid'].abs().describe())
# data.to_csv('validation.csv')
# 
# =============================================================================

print('using %s'%str(time.time() - s))