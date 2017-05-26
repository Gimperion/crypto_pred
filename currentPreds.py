#!/usr/bin/env python

import datetime
import tensorflow as tf
import numpy as np
import pandas as pd
import pyodbc
from keras.models import Sequential, Model
from keras.layers import Dense, LSTM, Dense, TimeDistributed, GRU, Dropout, RepeatVector
from keras.models import model_from_json

cnxn = pyodbc.connect('DSN=cryptopred')

current_frames = pd.read_sql("SELECT * FROM polo_current;", cnxn)

X = np.zeros((1,144, 32), dtype=np.float64)
for index, row in current_frames.iterrows():
	for j,i in enumerate(row):
		if j > 0:
			X[0][index][j-1] = i

# load json and create model
json_file = open('models/model_1495818974.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("models/model_1495818974.h5")
print("Loaded model from disk")
