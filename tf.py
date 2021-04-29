# tf.py uses tensorflow to build a neural network Ml model

import pandas as pd
import numpy as np

# Make numpy values easier to read.
np.set_printoptions(precision=3, suppress=True)

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.utils import to_categorical

df = pd.read_csv('LongGameData.csv')

X_data = df.iloc[:,:32].values # 104
y_data = df.iloc[:,32].values

KNOWN_SIZE = len(y_data)
indices = np.random.permutation(KNOWN_SIZE)
X_known = X_data[indices]
y_known = y_data[indices]


TRAIN_FRACTION = 0.90
TRAIN_SIZE = int(TRAIN_FRACTION*KNOWN_SIZE)
TEST_SIZE = KNOWN_SIZE - TRAIN_SIZE   
X_train = X_known[:TRAIN_SIZE]
y_train = y_known[:TRAIN_SIZE]

X_test = X_known[TRAIN_SIZE:]
y_test = y_known[TRAIN_SIZE:]

network = models.Sequential()
network.add(layers.Dense(32, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(32, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))
network.compile(optimizer='adam',
                loss='categorical_crossentropy'
                # metrics=['accuracy']
                )
        
network = models.Sequential()



network.fit(X_train, y_train, epochs=5, batch_size=128)