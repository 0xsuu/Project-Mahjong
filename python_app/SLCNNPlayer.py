#!/usr/bin/env python3

import sys
sys.path.append("../../build_mahjong")
sys.path.append("../../build_players")
sys.path.append("../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

from keras.models import load_model

import numpy as np

def expandHandToCSV(byteHand):
    retHand = []
    for i in byteHand:
        i = i.getData()
        # Convert to onehot encoding.
        converted_hand = 0
        converted_hand = 1 << (2 - ((i & 0b11000000) >> 6))
        converted_hand <<= 13
        converted_hand |= 1 << (3 - ((i & 0b110000) >> 4) + 9)
        converted_hand |= 1 << (9 - (i & 0b1111))
        retHand += list(bin(converted_hand)[2:].zfill(16))
    return retHand

def transformCSVHandToCNNMatrix(csvHand):
    csvHand = np.array([csvHand])
    return csvHand.reshape(csvHand.shape[0], 14, 16, 1)

class SLCNNPlayer(Player):
    def __init__(self, playerName):
        super(SLCNNPlayer, self).__init__(playerName)
        self.model = load_model("../supervised_learning/CNNModel.h5")
        self.model.load_weights("../supervised_learning/CNNModelWeights.h5")
    def onTurn(self, this, playerID, tile):
        if playerID == this.getID():
            if this.getHand().testWin():
                return Action(ActionState.Win, Tile())

            handData = this.getHand().getData()
            it = int(self.model.predict_classes(transformCSVHandToCNNMatrix(expandHandToCSV(handData)), verbose = 0)[0]);
            #print("Choosing... " + handData[0].getPrintable())

            return Action(ActionState.Discard, handData[it])
        else:
            return Action()
    def onOtherPlayerMakeAction(self, playerID, playerName, action):
        return Action()

