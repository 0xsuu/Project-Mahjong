#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD

import numpy as np
from numpy import genfromtxt

from sklearn.utils import shuffle

def train():
    model = Sequential()
    model.add(Convolution2D(32, 1, 3, border_mode='valid', input_shape=(1, 14, 8)))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 1, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(14, activation='sigmoid'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    X = genfromtxt('./train_data/n100X.csv', delimiter=',')
    y = genfromtxt('./train_data/n100y.csv', delimiter=',')

    X, y = shuffle(X, y, random_state = 0)
    
    X_train = X[5000:]
    y_train = y[5000:]
    X_cv = X[0: 5000]
    y_cv = y[0: 5000]

    X_train = X_train.reshape(X_train.shape[0], 1, 14, 8)
    X_cv = X_cv.reshape(X_cv.shape[0], 1, 14, 8)

    model.fit(X_train, y_train, validation_data=(X_cv, y_cv), batch_size=128, nb_epoch=15)

    print(model.evaluate(X_cv, y_cv))

    model.save('CNNModel.h5')
    model.save_weights('CNNModelWeights.h5')

train()

