#!/usr/bin/env python

import datetime
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM, TimeDistributed, GRU
from keras.layers import Dropout, Input, Concatenate, Reshape, Multiply, Permute
from keras.layers import Lambda, RepeatVector, Flatten


def SaveModel(model, fname="model"):
	dt = str(int(datetime.datetime.utcnow().timestamp()))
	model_json = model.to_json()
	with open("models/"+fname+"_"+dt+".json", "w") as json_file:
		json_file.write(model_json)

	model.save_weights("models/"+fname+"_"+dt+".h5")

df = pd.read_csv("data/polo_prices.csv")

X = np.zeros((len(df), 32), dtype=np.float64)

for index, row in df.iterrows():
	for j,i in enumerate(row):
		if j > 0:
			X[index][j-1] = i

in_frames = 288
out_frames = 12

dataX = []
dataY = []

for i in range(0, len(X)-(in_frames + out_frames)):
	addX = np.array(X[i:(i+in_frames)])
	addY = np.zeros((out_frames, 7), dtype=np.float64)
	for j in range(i+in_frames, i+(in_frames + out_frames)):
		for k in range(0,7):
			if addX[-1,k*4] == 0:
				addY[j-in_frames-i, k] = 0
			else:
				addY[j-in_frames-i, k] = X[j,k*4]/addX[-1,k*4] - 1
	for k in range(0,7):
		addX[:,k*4] = np.divide(addX[:,k*4], addX[-1,k*4])
	if not np.any(np.isnan(addX)):
		dataX.append(addX)
		dataY.append(addY)

dataX = np.array(dataX)
dataY = np.array(dataY)



### START MODEL ###
predictor = Sequential()
predictor.add(LSTM(256, input_shape=(288, 32), recurrent_dropout=0.2, dropout=0.25, activation="tanh"))
predictor.add(Dense(512, activation="tanh"))
predictor.add(Dropout(0.1))
predictor.add(RepeatVector(12))
predictor.add(LSTM(256, activation="tanh", return_sequences=True))
predictor.add(TimeDistributed(Dense(dataY.shape[2], activation='softmax')))
predictor.compile(optimizer='adam', loss='mean_squared_error')

predictor.summary()

predictor.fit(dataX, dataY,epochs=300,batch_size=250,shuffle=True)
## save to disk
SaveModel(predictor)
