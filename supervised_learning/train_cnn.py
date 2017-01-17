#!/usr/bin/env python3

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.models import load_model
from keras import backend as K

import numpy as np
from numpy import genfromtxt

from sklearn.utils import shuffle

import sys

def train():
    K.set_image_dim_ordering('th')

    model = Sequential()
    model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(1, 14, 8)))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
    model.add(Dropout(0.25))

#    model.add(Convolution2D(64, 3, 1, border_mode='same'))
#    model.add(Activation('relu'))
#    model.add(Convolution2D(64, 3, 1))
#    model.add(Activation('relu'))
#    model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
#    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(14, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adadelta',
                  metrics=['accuracy'])

    if len(sys.argv) > 1 and sys.argv[1] == "load":
        print("Loading previous weights...")
        model.load_weights("CNNModelWeights.h5")

    print("Loading Data...")
    X = genfromtxt('./train_data/n4X.csv', delimiter=',')
    y = genfromtxt('./train_data/n4y.csv', delimiter=',')
    print("Finished loading data.")

    X, y = shuffle(X, y, random_state = 0)

    totalSize = int(len(X))
    testSetSize = int(totalSize / 10)

    X_train = X[testSetSize:]
    y_train = y[testSetSize:]
    X_cv = X[0: testSetSize]
    y_cv = y[0: testSetSize]

    X_train = X_train.reshape(X_train.shape[0], 1, 14, 8)
    X_cv = X_cv.reshape(X_cv.shape[0], 1, 14, 8)

    model.fit(X_train, y_train, validation_data=(X_cv, y_cv), batch_size=128, nb_epoch=10)

    print(model.evaluate(X_cv, y_cv))

    model.save('CNNModel.h5')
    model.save_weights('CNNModelWeights.h5')

train()

