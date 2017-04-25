#!/usr/bin/env python3

import gc
from keras.models import load_model

import mahjong_hand_converter as converter

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

