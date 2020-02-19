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

from CO2_Processing import *
X_train,X_test,y_train,y_test = process_for_ML_test()

model = Sequential()
model.add(LSTM(128,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1))
opt = tf.keras.optimizers.Adam(lr=1e-3,decay=1e-5)
model.compile(loss='mse',optimizer=opt,metrics=['accuracy'])
model.fit(X_train,y_train,epochs=10,batch_size=20,validation_data=(X_test,y_test),verbose=0)


from keras.models import model_from_json
model_json = model.to_json()
with open("ML_Models/model1.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("ML_Models/model1.h5")
print("Saved model to disk")
