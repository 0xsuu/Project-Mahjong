#!/usr/bin/env python

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD

import numpy as np
from numpy import genfromtxt

def train():
    model = Sequential()
    model.add(Dense(448, input_dim=112))
    model.add(Activation('softmax'))
    model.add(Dense(896))
    model.add(Activation('softmax'))
    model.add(Dense(448))
    model.add(Activation('softmax'))
    model.add(Dense(224))
    model.add(Activation('softmax'))
    model.add(Dense(56))
    model.add(Activation('softmax'))
    model.add(Dense(14, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=SGD(lr=0.1),
                  metrics=['accuracy'])

    X = genfromtxt('./train_data/n100X.csv', delimiter=',')
    y = genfromtxt('./train_data/n100y.csv', delimiter=',')
    
    X_train = X[0: 1000]
    y_train = y[0: 1000]

    model.fit(X[1000:], y[1000:], batch_size=128, nb_epoch=15)

    print model.predict(X_train)
    print model.evaluate(X_train, y_train)

    model.save('SLModel.h5')
    model.save_weights('SLModelWeights.h5')

train()

