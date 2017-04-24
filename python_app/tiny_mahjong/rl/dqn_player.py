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

from collections import deque
from random import sample

from game import *
import os.path
from datetime import datetime

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras import backend as K

import numpy as np

import tensorflow as tf

DQN_MODEL_FILE = "dqn_model.h5"
DQN_WEIGHTS_FILE = "dqn_weights.h5"

TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
SELF_PLAY = 500

EPSILON_INITIAL = 0.01
EPSILON_FINAL = 0.01
EPSILON_DECAY_STEP = 100000
REPLAY_MEMORY_SIZE = 100000
BATCH_SIZE = 32
TARGET_UPDATE_INTERVAL = 100
GAMMA = 0.99
USE_DOUBLE_DQN = False


class DQNPlayer(Player):
    def __init__(self, name, mode):
        Player.__init__(self, name)
        self._mode = mode
        if os.path.isfile(DQN_MODEL_FILE):
            self._model = load_model(DQN_MODEL_FILE)
        else:
            self._model = self._create_keras_model()
            self._model.save(DQN_MODEL_FILE)

        if os.path.isfile(DQN_WEIGHTS_FILE):
            self._model.load_weights(DQN_WEIGHTS_FILE)

        self._target_model = self._create_keras_model()
        self._target_model.set_weights(self._model.get_weights())

        self.current_episode = 0
        self._epsilon = EPSILON_INITIAL
        self._replay_memory = deque()

        self.prev_hand = None
        self.prev_action = None
        self._step = None
        self._total_step = 0

        self._max_q_history = []
        self._win_round = 0
        self._drain_round = 0
        self._total_reward = 0

        self._writer = tf.summary.FileWriter("./logs/" + str(datetime.now()))

    @staticmethod
    def _create_keras_model():
        K.set_image_dim_ordering('tf')

        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), padding='same', input_shape=(5, 18, 1)))
        model.add(Activation('relu'))
        model.add(Conv2D(64, kernel_size=(3, 3)))
        model.add(Activation('relu'))

        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))

        model.add(Dense(5, activation='linear'))

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.00025),
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _pre_process(hand):
        reshaped_input = np.array([])
        for t in hand:
            binarized = [0] * 18
            binarized[int(t) - 1] = 1
            if reshaped_input.size == 0:
                reshaped_input = np.array(binarized)
            else:
                reshaped_input = np.append(reshaped_input, binarized, axis=0)
        reshaped_input = reshaped_input.reshape(1, 5, 18, 1)
        return reshaped_input

    def _epsilon_greedy_choose(self, hand):
        q_values = self._model.predict(self._pre_process(hand))[0]

        if np.random.uniform(0, 1.0, 1)[0] < self._epsilon and self._mode == TRAIN:
            return random.randint(0, 4)
        else:
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
                print("Q values:", q_values, "\ndiscarding", choice)
                print()
            return choice

    def append_memory_and_train(self, observation, action, reward, observation_next, done):
        if observation is None or observation_next is None:
            return
        observation = self._pre_process(observation)[0]
        observation_next = self._pre_process(observation_next)[0]
        self._replay_memory.append((observation, action, reward, observation_next, done))
        if len(self._replay_memory) > REPLAY_MEMORY_SIZE:
            self._replay_memory.popleft()

        # Mini batch train.
        if len(self._replay_memory) > BATCH_SIZE and self._total_step % 4 == 0:
            mini_batch = sample(list(self._replay_memory), BATCH_SIZE)
            observation_batch = np.array([m[0] for m in mini_batch])
            action_batch = [m[1] for m in mini_batch]
            reward_batch = [m[2] for m in mini_batch]
            observation_next_batch = np.array([m[3] for m in mini_batch])

            q_values = self._model.predict(observation_batch)
            self._max_q_history.append(np.max(q_values))
            next_q_values_target = self._target_model.predict(observation_next_batch)
            next_q_values = self._model.predict(observation_next_batch)
            for i in range(BATCH_SIZE):
                if mini_batch[i][4]:  # done.
                    q_values[i][action_batch[i]] = reward_batch[i]
                else:
                    if USE_DOUBLE_DQN:
                        q_values[i][action_batch[i]] = \
                            reward_batch[i] + \
                            GAMMA * next_q_values_target[i][np.argmax(next_q_values[i])]
                    else:
                        q_values[i][action_batch[i]] = \
                            reward_batch[i] + \
                            GAMMA * np.max(next_q_values_target[i])
            self._model.train_on_batch(observation_batch, q_values)

        # Periodically update target network.
        if self._total_step % TARGET_UPDATE_INTERVAL == 0:
            self._target_model.set_weights(self._model.get_weights())

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)
        self.current_episode += 1
        self.prev_hand = None
        self.prev_action = None
        self._step = 0

    def tile_picked(self):
        Player.tile_picked(self)
        self._step += 1
        self._total_step += 1
        if self.test_win():
            self.append_memory_and_train(self.prev_hand, self.prev_action, 1.0, self.hand, True)
            return WIN, -1
        else:
            action = self._epsilon_greedy_choose(self.hand)
            if self._epsilon > EPSILON_FINAL:
                self._epsilon -= (EPSILON_INITIAL - EPSILON_FINAL) / EPSILON_DECAY_STEP
            self.append_memory_and_train(self.prev_hand, self.prev_action, -0.01, self.hand, False)
            self.prev_hand = self.hand
            self.prev_action = action
            return DISCARD, action

    def game_ends(self, win, drain=False):
        Player.game_ends(self, win, drain)

        # Summary.
        if win:
            self._win_round += 1
        if drain:
            self._drain_round += 1
        if self._mode == TRAIN:
            if len(self._max_q_history) > 0:
                average_max_q = sum(self._max_q_history) / len(self._max_q_history)
            else:
                average_max_q = 0
            summary = tf.Summary()
            summary.value.add(tag="Average Max Q", simple_value=average_max_q)
            summary.value.add(tag="Steps per episode", simple_value=self._step)
            summary.value.add(tag="Win rate",
                              simple_value=self._win_round * 1.0 / self.current_episode)
            summary.value.add(tag="Drain rate",
                              simple_value=self._drain_round * 1.0 / self.current_episode)
            self._writer.add_summary(summary, self.current_episode)
            self._writer.flush()
            print("Epsilon:", self._epsilon, "Average max Q:", average_max_q)
            self._max_q_history = []

            if self.current_episode % 100 == 0:
                print("Finished", self.current_episode, "episodes.")
                self._model.save_weights(DQN_WEIGHTS_FILE)

        elif self._mode == PLAY:
            print(self.name + ":")
            if win:
                print("Won!")
        elif self._mode == EVAL:
            print("Win rate:", str(self.rounds_won * 100.0 / self.current_episode) + "%")
        elif self._mode == DEBUG:
            if win:
                print(self.name, "won!")
        elif self._mode == SELF_PLAY:
            if self.current_episode % 1000 == 0:
                self._model.load_weights(DQN_WEIGHTS_FILE)
