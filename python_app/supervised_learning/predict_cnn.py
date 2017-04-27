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

import sys

from keras.models import load_model
sys.path.append("../")

from utils import mahjong_hand_converter as converter

model = load_model("cnn_model.h5")
model.load_weights("cnn_weights.h5")

hand = input("Input your hand, split by space: ")

inputs = converter.transform_one_hot_to_cnn_matrix(
        converter.transform_hand_to_one_hot(converter.to_mahjong_hand(hand.split(" "))))
print(inputs)
proba = model.predict_proba(inputs)[0]
p_class = int(model.predict_classes(inputs)[0])
print(proba)
print("Choose NO." + str(p_class) + " - " + hand.split(" ")[p_class] + " with probability: " + str(proba[p_class] * 100) + "%")
