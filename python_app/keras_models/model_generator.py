#!/usr/bin/env python3

#  Copyright 2017 Project Mahjong. All rights reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from keras.models import Sequential
from keras.layers import Conv2D, Dense, Activation, Flatten
from keras.optimizers import Adam
from keras import backend

from helper import *

TM_DEFAULT_INPUT_SHAPE = (5, 18, 1)
TM_DEFAULT_OUTPUT_NUMBER = 5
TM_DEFAULT_LAYER_CONFIGURATIONS = (32, 64, 256)
TM_DEFAULT_OPTIMIZER = Adam
TM_DEFAULT_LEARNING_RATE = 0.00025


def tiny_mahjong_dqn_model(input_shape=TM_DEFAULT_INPUT_SHAPE,
                           output_number=TM_DEFAULT_OUTPUT_NUMBER,
                           layer_configurations=TM_DEFAULT_LAYER_CONFIGURATIONS,
                           optimizer=TM_DEFAULT_OPTIMIZER,
                           lr=TM_DEFAULT_LEARNING_RATE,
                           dim_ordering="tf"):
    backend.set_image_dim_ordering(dim_ordering)

    model = Sequential()
    model.add(Conv2D(layer_configurations[0], kernel_size=(3, 3), padding='same', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(layer_configurations[1], kernel_size=(3, 3)))
    model.add(Activation('relu'))

    model.add(Flatten())
    model.add(Dense(layer_configurations[2]))
    model.add(Activation('relu'))

    model.add(Dense(output_number, activation='linear'))

    model.compile(loss='mean_squared_error',
                  optimizer=optimizer(lr=lr),
                  metrics=['accuracy'])

    save_keras_model(TM_DQN_MODEL_NAME, model)
