#!/usr/bin/env python3

import numpy as np

from keras.models import load_model

import sys
sys.path.append("../python_app")

import MahjongHandConverter as converter

model = load_model("CNNModel.h5")
model.load_weights("CNNModelWeights.h5")

hand = input("Input your hand, split by space: ")

inputs = converter.transformCSVHandToCNNMatrix(converter.expandHandToCSV(converter.toMahjongHand(hand.split(" "))))
print(inputs)
proba = model.predict_proba(inputs)[0]
pClass = int(model.predict_classes(inputs)[0])
print(proba)
print("Choose NO." + str(pClass) + " - " + hand.split(" ")[pClass] + " with probability: " + str(proba[pClass] * 100) + "%")
