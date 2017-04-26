#!/usr/bin/env python3

from keras.models import load_model

from libgames import *
from libmahjong import *
from libplayers import *

from mahjong_hand_converter import *


class SLCNNPlayer(Player):
    def __init__(self, playerName):
        super(SLCNNPlayer, self).__init__(playerName)
        self.model = load_model("../../supervised_learning/cnn_model.h5")
        self.model.load_weights("../../supervised_learning/cnn_weights.h5")

    def onTurn(self, this, playerID, tile):
        if playerID == this.getID():
            if this.getHand().testWin():
                return Action(ActionState.Win, Tile())

            handData = this.getHand().getData()
            it = int(self.model.predict_classes(
                transform_one_hot_to_cnn_matrix(
                    transform_hand_to_one_hot(handData)), verbose=0)[0])

            return Action(ActionState.Discard, handData[it])
        else:
            return Action()

    def onOtherPlayerMakeAction(self, playerID, playerName, action):
        return Action()
