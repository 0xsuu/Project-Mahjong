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

from game import *
import os.path

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras import backend as K

TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
EPSILON = 0.01
GAMMA = 0.1
WIN_REWARD = 100
DISCARD_REWARD = -1
MCNN_MODEL_FILE = "mcnn_model.h5"
MCNN_WEIGHTS_FILE = "mcnn_weights.h5"


class MCNNPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode
        if os.path.isfile(MCNN_MODEL_FILE):
            self._model = load_model(MCNN_MODEL_FILE)
            self._model.load_weights(MCNN_WEIGHTS_FILE)
        else:
            self._model = self._create_keras_model()
            self._model.save(MCNN_MODEL_FILE)

        self.current_episode = 0
        self.hand_tuple_visits = {}
        self.gain = 0.0

    @staticmethod
    def _create_keras_model():
        K.set_image_dim_ordering('tf')

        model = Sequential()
        model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=(5, 18, 1)))
        model.add(Activation('relu'))
        model.add(Convolution2D(32, 3, 3))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="tf"))

        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))

        model.add(Dense(1, activation='linear'))

        model.compile(loss='mean_squared_error',
                      optimizer='RMSprop',
                      metrics=['accuracy'])

        return model

    def _get_hand_value(self, hand):
        reshaped_input = np.array([])
        for t in hand:
            binarized = [0]*18
            binarized[int(t) - 1] = 1
            if reshaped_input.size == 0:
                reshaped_input = np.array(binarized)
            else:
                reshaped_input = np.append(reshaped_input, binarized, axis=0)
        reshaped_input = reshaped_input.reshape(1, 5, 18, 1)
        return self._model.predict(reshaped_input, batch_size=1)[0][0]

    def _epsilon_greedy_choose(self):
        if np.random.uniform(0, 1.0, 1)[0] < EPSILON and self._mode == TRAIN:
            return int(np.random.uniform(0, 5.0, 1)[0])
        else:
            q_values = np.array([0.0, 0.0, 0.0, 0.0, 0.0], dtype="float16")
            for i in range(5):
                discarded_hand = np.delete(self.hand, i)
                max_reward = DISCARD_REWARD
                for picked_tile in range(1, 19):
                    if not self.has_tile_in_stack(picked_tile):
                        continue
                    picked_hand = np.append(discarded_hand, picked_tile)
                    picked_hand.sort()
                    if self.test_win_hand(picked_hand):
                        max_reward = WIN_REWARD
                    q_values[i] += self.get_pick_tile_probability(picked_tile) * \
                        self._get_hand_value(picked_hand)
                q_values[i] += max_reward
            # Choose the maximum Q's index as a policy.
            choice = np.random.choice(
                np.array([i for i, j in enumerate(q_values) if j == max(q_values)]))
            if self._mode == DEBUG:
                print(self.name)
                print("Hand    : ", end="")
                for i in self.hand:
                    if i <= 9:
                        print("A" + str(int(i)), end="  ")
                    else:
                        print("B" + str(int(i - 9)), end="  ")
                print()
                print("Current value:", self._get_hand_value(self.hand))
                print("Q values:", q_values, "\ndiscarding", choice)
                print()
            return choice

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self.current_episode += 1
        self.hand_tuple_visits = {}
        self.gain = 0.0

    def tile_picked(self):
        Player.tile_picked(self)
        if tuple(self.hand.tolist()) in self.hand_tuple_visits.keys():
            self.hand_tuple_visits[tuple(self.hand.tolist())] += 1
        else:
            self.hand_tuple_visits[tuple(self.hand.tolist())] = 1
        if self.test_win():
            self.gain = WIN_REWARD
            return WIN, -1
        else:
            self.gain = DISCARD_REWARD + GAMMA * self.gain
            return DISCARD, self._epsilon_greedy_choose()

    def game_ends(self, win, drain=False):
        Player.game_ends(self, win, drain)
        input_set = np.array([])
        for visited_hand_tuple in self.hand_tuple_visits:
            for t in list(visited_hand_tuple):
                binarized = [[0]*18]
                binarized[0][int(t) - 1] = 1
                if input_set.size == 0:
                    input_set = np.array(binarized)
                else:
                    input_set = np.append(input_set, binarized, axis=0)
        input_set = shuffle(input_set)
        input_set = input_set.reshape(int(input_set.shape[0]/5), 5, 18, 1)
        output_true_set = np.array([self.gain] * len(input_set))

        if self._mode == TRAIN:
            if input_set.size > 0:
                self._model.fit(input_set, output_true_set, batch_size=2, nb_epoch=10, verbose=0)
            if self.current_episode % 10 == 0:
                print("Finished", self.current_episode, "episodes.")
                self._model.save_weights(MCNN_WEIGHTS_FILE)

        elif self._mode == PLAY:
            print(self.name + ":")
            if win:
                print("Won!")
        elif self._mode == EVAL:
            print("Win rate:", str(self.rounds_won * 100.0 / self.current_episode) + "%")
        elif self._mode == DEBUG:
            if win:
                print(self.name, "won!")
