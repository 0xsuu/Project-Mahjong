#!/usr/bin/env python3

import numpy as np

def tileToByte(t):
    if t[0].isdigit():
        tValue = int(t[0])
    else:
        # Avoiding White Drage & West Wind, so change to Bai Dragon.
        if t[1] == "d" and t[0] == "w":
            tValue = 6
        else:
            tValue = {"e": 1, "s": 2, "w": 3, "n": 4, "r": 5, "b": 6, "g": 7}[t[0]]
    tType = {"m": 0, "p": 1, "s": 2, "w": 3, "d": 3}[t[1]]
    tMeld = 0
    if len(t) > 2:
        tMeld = int(t[2])
    return tMeld << 6 | tType << 4 | tValue

def toMahjongHand(hand):
    retHand = []
    for i in hand:
        retHand.append(tileToByte(i))
    retHand.sort()
    return retHand

def expandHandToCSV(byteHand):
    retHand = []
    for i in byteHand:
        retHand += list(bin(i)[2:].zfill(8))
    return retHand

from keras.models import load_model

model = load_model("MLPModel.h5")
model.load_weights("MLPModelWeights.h5")

hand = raw_input("Input your hand, split by space: ")

inputs = np.array([expandHandToCSV(toMahjongHand(hand.split(" ")))])
print(inputs)
print(model.predict_proba(inputs))

