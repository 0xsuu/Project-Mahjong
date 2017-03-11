#!/usr/bin/env python3

import sys
sys.path.append("../../build_mahjong")
sys.path.append("../../build_players")
sys.path.append("../../build_games")
from libmahjong import *
from libplayers import *
from libgames import *

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K
from keras.callbacks import TensorBoard

import numpy as np

def expandHandToCSV(byteHand):
    retHand = []
    for i in byteHand:
        retHand += list(bin(i.getData())[2:].zfill(8))
    return retHand

def transformCSVHandToCNNMatrix(csvHand):
    csvHand = np.array([csvHand])
    return csvHand.reshape(csvHand.shape[0], 1, 14, 8)

class MCNNPlayer(Player):
    def __init__(self, playerName):
        super(MCNNPlayer, self).__init__(playerName)
        self.X = np.array([[]])
        self.y = np.array([[]])
        self.set_model()
    
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
    
    def onRoundFinished(self, drained, winner):
        print("Win", self == winner)

    def set_model(self):
        K.set_image_dim_ordering('th')
    
        self.model = Sequential()
        self.model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(1, 14, 8)))
        self.model.add(Activation('relu'))
        self.model.add(Convolution2D(32, 3, 3))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
        self.model.add(Dropout(0.25))
        
        self.model.add(Flatten())
        self.model.add(Dense(128))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(14, activation='softmax'))
        
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='adadelta',
                           metrics=['accuracy'])

