#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import SGD
from keras.regularizers import l2, activity_l2

import numpy as np
from numpy import genfromtxt

from sklearn.utils import shuffle

def train():
    model = Sequential()
    model.add(Dense(2000, input_dim=112, W_regularizer=l2(0.01), activity_regularizer=activity_l2(0.01)))
    model.add(Activation('relu'))
#    model.add(Dense(4000))
#    model.add(Activation('relu'))
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
                  optimizer='adam',
                  metrics=['accuracy'])

    X = genfromtxt('./train_data/n100X.csv', delimiter=',')
    y = genfromtxt('./train_data/n100y.csv', delimiter=',')

    X, y = shuffle(X, y, random_state = 0)

    X_train = X[5000:]
    y_train = y[5000:]
    X_cv = X[0: 5000]
    y_cv = y[0: 5000]

    model.fit(X_train, y_train, validation_data=(X_cv, y_cv), batch_size=128, nb_epoch=10)

    print(model.evaluate(X_cv, y_cv))

    model.save('MLPModel.h5')
    model.save_weights('MLPModelWeights.h5')

train()

