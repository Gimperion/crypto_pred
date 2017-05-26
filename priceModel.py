import tensorflow as tf
from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM, TimeDistributed, GRU
from keras.layers import Dropout, Input, Concatenate, Reshape, Multiply, Permute
from keras.layers import Lambda, RepeatVector, Flatten


def SaveModel(model, fname="model"):
	model_json = model.to_json()
	with open("models/"+fname+".json", "w") as json_file:
		json_file.write(model_json)

	model.save_weights("models/"+fname+".h5")


df = pd.read_csv("data/polo_prices.csv")

X = np.zeros((len(df), 32), dtype=np.float64)

for index, row in df.iterrows():
	for j,i in enumerate(row):
		if j > 0:
			X[index][j-1] = i

dataX = []
dataY = []

for i in range(0, len(X)-150):
	addX = X[i:(i+144)]
	addY = []
	for j in range(i+144, i+150):
		tmp = np.zeros((7), dtype=np.float64)
		for k in range(0,7):
			# denom_fix = addX[-1,k*4]
			# if denom_fix == 0:
			# 	denom_fix = 0.00000000001
			#tmp[k] = (X[j,k*4] - addX[-1,k*4])/denom_fix
			tmp[k] = X[j,k*4]
		addY.append(tmp)
	dataX.append(addX)
	dataY.append(addY)

dataX = np.array(dataX)
dataY = np.array(dataY)

### MODEL
predictor = Sequential()
predictor.add(LSTM(256, input_shape=(144, 32), recurrent_dropout=0.25, dropout=0.2, activation="tanh"))
predictor.add(Dense(512, activation="tanh"))
predictor.add(Dropout(0.1))
predictor.add(RepeatVector(6))
predictor.add(GRU(256, activation="tanh", return_sequences=True))
predictor.add(TimeDistributed(Dense(dataY.shape[2], activation='linear')))
predictor.compile(optimizer='adam', loss='mean_squared_error')

predictor.summary()

predictor.fit(dataX, dataY,epochs=300,batch_size=1000,shuffle=True)
## save to disk
SaveModel(predictor)
