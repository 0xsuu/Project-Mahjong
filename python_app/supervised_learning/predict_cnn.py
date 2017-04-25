#!/usr/bin/env python3

import numpy as np

from keras.models import load_model

import sys
sys.path.append("../")

import mahjong_hand_converter as converter

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

