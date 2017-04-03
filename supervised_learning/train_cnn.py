#!/usr/bin/env python3

import sys

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.callbacks import TensorBoard

from numpy import genfromtxt

from sklearn.utils import shuffle

def train():
    K.set_image_dim_ordering('tf')

    model = Sequential()
    model.add(Conv2D(64, kernel_size=(3, 3), padding='same', input_shape=(14, 16, 1)))
    model.add(Activation('relu'))
    model.add(Conv2D(64, kernel_size=(3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

#    model.add(Conv2D(64, 3, 1))
#    model.add(Activation('relu'))
#    model.add(Conv2D(64, 3, 1))
#    model.add(Activation('relu'))
#    model.add(MaxPooling2D(pool_size=(2, 2)))
#    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
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
    X = genfromtxt('./train_data/n2X.csv', delimiter=',')
    y = genfromtxt('./train_data/n2y.csv', delimiter=',')
    print("Finished loading data.")

    X, y = shuffle(X, y)

    total_size = int(len(X))
    test_set_size = int(total_size / 10)

    X_train = X[test_set_size:]
    y_train = y[test_set_size:]
    X_cv = X[0: test_set_size]
    y_cv = y[0: test_set_size]

    X_train = X_train.reshape(X_train.shape[0], 14, 16, 1)
    X_cv = X_cv.reshape(X_cv.shape[0], 14, 16, 1)

    tf_board_callback = TensorBoard(log_dir='./logs', \
            histogram_freq=0, write_graph=True, write_images=True)

    model.fit(X_train, y_train, validation_data=(X_cv, y_cv), \
            callbacks=[tf_board_callback], batch_size=128, epochs=10)

    print(model.evaluate(X_cv, y_cv))

    model.save('CNNModel.h5')
    model.save_weights('CNNModelWeights.h5')

train()
