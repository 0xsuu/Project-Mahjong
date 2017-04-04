#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append("../../build_mahjong")
sys.path.append("../../build_players")
sys.path.append("../../build_games")
sys.path.append("../python_app")
from libmahjong import *
from libplayers import *
from libgames import *
from MahjongHandConverter import *

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K

import numpy as np

from sklearn.utils import shuffle

TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
EPSILON_INITIAL = 0.5
EPSILON_FINAL = 0.01
EPSILON_DECAY_STEP = 100000
DQCNN_MODEL_FILE = "dqcnn_model.h5"
DQCNN_WEIGHTS_FILE = "dqcnn_weights.h5"


class DQCNNPlayer(Player):
    def __init__(self, name, mode):
        super(DQCNNPlayer, self).__init__(name)
        self._mode = mode
        self.model = self.make_model()
        if os.path.isfile(DQCNN_MODEL_FILE):
            self._model = load_model(DQCNN_MODEL_FILE)
        else:
            self._model = self.make_model()
            self._model.save(DQCNN_MODEL_FILE)

        if os.path.isfile(DQCNN_WEIGHTS_FILE):
            self._model.load_weights(DQCNN_WEIGHTS_FILE)

        self.current_episode = 0
        self.epsilon = EPSILON_INITIAL
        self.last_hand = None
        self.last_discard = None
        self.batch_train = np.array([])
        self.batch_class = np.array([])
        self.is_discard = False

    @staticmethod
    def make_model():
        K.set_image_dim_ordering('tf')

        model = Sequential()
        model.add(Conv2D(64, kernel_size=(3, 3), padding='same', input_shape=(14, 16, 1)))
        model.add(Activation('relu'))
        model.add(Conv2D(64, kernel_size=(3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(14, activation='linear'))

        model.compile(loss='mse',
                      optimizer='rmsprop',
                      metrics=['accuracy'])
        return model

    @staticmethod
    def get_q_values(model, hand):
        return model.predict(transformCSVHandToCNNMatrix(expandHandToCSV(hand)))[0]

    @staticmethod
    def make_epsilon_greedy_choice(epsilon, mode, model, hand):
        if np.random.uniform(0, 1.0, 1)[0] < epsilon and mode == TRAIN:
            return int(np.random.uniform(0, 5.0, 1)[0])
        else:
            q_values = DQCNNPlayer.get_q_values(model, hand)
            choice = np.random.choice(
                np.array([i for i, j in enumerate(q_values) if j == max(q_values)]))
            return choice

    def append_last_hand(self):
        if self.last_hand is not None:
            if self.batch_train.size > 0:
                self.batch_train = \
                    np.append(
                        self.batch_train,
                        transformCSVHandToCNNMatrix(
                            expandHandToCSV(self.last_hand)),
                        axis=0)
            else:
                self.batch_train = \
                    np.array(transformCSVHandToCNNMatrix(expandHandToCSV(self.last_hand)))
            return True
        else:
            return False

    def onTurn(self, this, playerID, tile):
        if playerID == this.getID():
            classes = np.array([])
            if self.append_last_hand():
                classes = self.get_q_values(self.model, self.last_hand)
            if this.getHand().testWin():
                if classes.size > 0:
                    classes[self.last_discard] = 1
                    if self.batch_class.size > 0:
                        self.batch_class = np.append(self.batch_class, [classes], axis=0)
                    else:
                        self.batch_class = np.array([classes])
                self.game_ends(True, False)
                return Action(ActionState.Win, Tile())
            else:
                if classes.size > 0:
                    classes[self.last_discard] = np.max(
                        self.get_q_values(self.model, this.getHand().getData()))
                    if self.batch_class.size > 0:
                        self.batch_class = np.append(self.batch_class, [classes], axis=0)
                    else:
                        self.batch_class = np.array([classes])
                it = self.make_epsilon_greedy_choice(
                    self.epsilon, self._mode, self.model, this.getHand().getData())
                self.epsilon -= (EPSILON_INITIAL - EPSILON_FINAL) / EPSILON_DECAY_STEP
                self.is_discard = True
                self.last_hand = list(this.getHand().getData())
                self.last_discard = it
                return Action(ActionState.Discard, list(this.getHand().getData())[it])
        else:
            return Action()

    def onOtherPlayerMakeAction(self, playerID, playerName, action):
        if playerID == -1 and playerName == "":
            if self.append_last_hand():
                classes = self.get_q_values(self.model, self.last_hand)
                classes[self.last_discard] = 0.1
                if self.batch_class.size > 0:
                    self.batch_class = np.append(self.batch_class, [classes], axis=0)
                else:
                    self.batch_class = np.array([classes])
            self.game_ends(False, False, True)
            return Action()

        if action.getActionState() == ActionState.Win:
            if self.is_discard:
                if self.append_last_hand():
                    classes = self.get_q_values(self.model, self.last_hand)
                    classes[self.last_discard] = -1
                    if self.batch_class.size > 0:
                        self.batch_class = np.append(self.batch_class, [classes], axis=0)
                    else:
                        self.batch_class = np.array([classes])
                self.game_ends(False, True)
            else:
                if self.append_last_hand():
                    classes = self.get_q_values(self.model, self.last_hand)
                    classes[self.last_discard] = 0.1
                    if self.batch_class.size > 0:
                        self.batch_class = np.append(self.batch_class, [classes], axis=0)
                    else:
                        self.batch_class = np.array([classes])
                self.game_ends(False, False)
        else:
            self.is_discard = False

        return Action()

    def game_ends(self, win, lose, drain=False):
        self.is_discard = False
        self.last_hand = None
        self.last_discard = None
        self.current_episode += 1
        if self._mode == TRAIN:
            if self.current_episode % 100 == 0:
                print("Finished", self.current_episode, "episodes.")
                if self.batch_train.size > 0:
                    self.batch_train, self.batch_class = shuffle(self.batch_train,
                                                                 self.batch_class)
                    self.model.fit(self.batch_train, self.batch_class, batch_size=16, epochs=1)
                    self.batch_train = np.array([])
                    self.batch_class = np.array([])
                    self.model.save_weights(DQCNN_WEIGHTS_FILE)
