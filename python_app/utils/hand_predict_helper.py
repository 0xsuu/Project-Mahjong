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

import gc

from keras.models import load_model

from utils import mahjong_hand_converter as converter

model = load_model("cnn_model.h5")
model.load_weights("cnn_weights.h5")

hand_string = input("Input your initial hand, split by space: ")
initial_hand = converter.to_mahjong_hand(hand_string.split(" "))

while 1:
    print("Current Hand:", converter.to_string_hand(initial_hand))
    picked_tile = None
    try:
        picked_tile = input("Input the tile you picked: ")
    except KeyboardInterrupt:
        gc.collect()
        print("\nBye!")
        quit(0)
    initial_hand.append(converter.tile_to_byte(picked_tile))
    initial_hand.sort()

    print("Current Hand:", converter.to_string_hand(initial_hand))
    inputs = converter.transform_one_hot_to_cnn_matrix(
        converter.transform_hand_to_one_hot(initial_hand))
    probabilities = model.predict_proba(inputs)[0]
    p_class = int(model.predict_classes(inputs)[0])
    print(probabilities)
    print("Choose NO." + str(p_class) + " - " + converter.byte_to_tile(initial_hand[p_class]) +
          " with probabilities: " + str(probabilities[p_class] * 100) + "%")
    initial_hand.pop(p_class)

