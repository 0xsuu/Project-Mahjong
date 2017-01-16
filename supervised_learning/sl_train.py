#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

import numpy as np
from numpy import genfromtxt

from sklearn.utils import shuffle

def train():
    model = Sequential()
    model.add(Dense(2000, input_dim=112))
    model.add(Activation('relu'))
    model.add(Dense(4000))
    model.add(Activation('relu'))
    model.add(Dense(3000))
    model.add(Activation('relu'))
    model.add(Dense(1500))
    model.add(Activation('relu'))
    model.add(Dense(700))
    model.add(Activation('relu'))
    model.add(Dense(300))
    model.add(Activation('relu'))
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dense(14, activation='sigmoid'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(lr=0.1),
                  metrics=['accuracy'])

    X = genfromtxt('./train_data/n100X.csv', delimiter=',')
    y = genfromtxt('./train_data/n100y.csv', delimiter=',')

    X, y = shuffle(X, y, random_state = 0)

    X_train = X[0: 1000]
    y_train = y[0: 1000]

    model.fit(X[1000:], y[1000:], batch_size=128, nb_epoch=15)

    print(model.predict(X_train))
    print(model.evaluate(X_train, y_train))

    model.save('SLModel.h5')
    model.save_weights('SLModelWeights.h5')

train()

