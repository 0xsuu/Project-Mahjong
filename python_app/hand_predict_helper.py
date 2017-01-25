#!/usr/bin/env python3

import numpy as np

import MahjongHandConverter as converter

import gc

from keras.models import load_model

model = load_model("CNNModel.h5")
model.load_weights("CNNModelWeights.h5")

handString = input("Input your initial hand, split by space: ")
initialHand = converter.toMahjongHand(handString.split(" "))

while 1:
    print("Current Hand:", converter.toStringHand(initialHand))
    try:
        pickedTile = input("Input the tile you picked: ")
    except:
        print("\nBye!")
        quit(0)
    initialHand.append(converter.tileToByte(pickedTile))
    initialHand.sort()

    print("Current Hand:", converter.toStringHand(initialHand))
    inputs = converter.transformCSVHandToCNNMatrix(converter.expandHandToCSV(initialHand))
    proba = model.predict_proba(inputs)[0]
    pClass = int(model.predict_classes(inputs)[0])
    print(proba)
    print("Choose NO." + str(pClass) + " - " + converter.byteToTile(initialHand[pClass]) + " with probability: " + str(proba[pClass] * 100) + "%")
    initialHand.pop(pClass)

gc.collect()
