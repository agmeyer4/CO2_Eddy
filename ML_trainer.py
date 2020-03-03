import CO2_Processing


import tensorflow as tf
from tensorflow import keras
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense, Dropout, LSTM
#IMPORT NECESSARY PACKAGES
import CO2_functions
import CO2_Processing
import pandas as pd
from CO2_functions import *
from CO2_Processing import *
import matplotlib.pyplot as plt
import pickle
import numpy as np
import sklearn
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

pn=6
print('Retrieving and processing data')
X_train,X_test,y_train,y_test,min_max_scalar = process_for_ML_test(['Pic_CO2','ANEM_X','ANEM_Y','ANEM_Z','wd','ws'],15,pn)


print('building and fitting model')
dropout_rate = 0.2
activation = 'relu'
opt = 'Adam'
epochs = 10
batch_size = 20
LSTM_layers = 1
dropout_layers = 1
dropout_rate = 0.2
dense_layers = 1

model = Sequential()
model.add(LSTM(128,activation=activation))
model.add(Dropout(dropout_rate))
model.add(Dense(1,activation = 'sigmoid'))
opt = tf.keras.optimizers.Adam(lr=1e-3,decay=1e-5)
model.compile(loss='mse',optimizer=opt,metrics=['accuracy'])
history = model.fit(X_train,y_train,epochs=epochs,batch_size=batch_size,validation_data=(X_test,y_test),verbose=2)
print('model fit complete: \nDropout Rate = {}\nbatch_size={}\nepochs={}\nactivation={}\nLSTM_layers={}\ndropout_layers={}\dense_layers={}'.format(dropout_rate,batch_size,epochs,activation,LSTM_layers,dropout_layers,dense_layers))

name = "Dense_sigmoid_PN{}BS{}E{}".format(pn,batch_size,epochs)
from keras.models import model_from_json
import json
hist_df = pd.DataFrame(history.history)
model_json = model.to_json()
with open("ML_Models/{}_model.json".format(name), "w") as json_file:
    json_file.write(model_json)
model.save_weights("ML_Models/{}_model.h5".format(name))
with open('ML_Models/{}_hist.json'.format(name), 'w') as f:
    hist_df.to_json(f)
print("Saved model to disk")

