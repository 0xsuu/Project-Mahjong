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

"""
This module contains all the constants and some utility functions.
"""

import os

from keras.models import load_model

TM_DQN_MODEL_NAME = "tm_dqn_model.h5"  # Tiny Mahjong DQN model file name.


def _full_path_of(model_name):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + model_name


def load_keras_model(model_name, model_generating_function=None):
    if os.path.isfile(TM_DQN_MODEL_NAME):
        return load_model(_full_path_of(model_name))
    elif model_generating_function is not None:
        model_generating_function()
        return load_model(_full_path_of(model_name))
    else:
        raise AttributeError("No saved models or model generating function provided!")


def save_keras_model(model_name, model):
    model.save(_full_path_of(model_name))
