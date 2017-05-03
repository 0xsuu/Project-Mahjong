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

import sys

sys.path.append("../")

from double_dqn import *

from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from keras.optimizers import Adam

import numpy as np
from skimage import color, transform

import gym

RAW_WIDTH = 84
RAW_HEIGHT = 84


class DQNBreakout(DoubleDQN):
    def __init__(self, action_count, weights_file_path="breakout_weights.h5",
                 mode=TRAIN, load=True):
        DoubleDQN.__init__(self, action_count, weights_file_path,
                           target_update_interval=1000, gamma=0.9, mode=mode,
                           load_previous_model=load)

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(8, 8), padding="same", strides=(4, 4),
                         input_shape=(RAW_WIDTH, RAW_HEIGHT, 1),
                         activation="relu", kernel_initializer="random_normal"))
        model.add(Conv2D(64, kernel_size=(4, 4), strides=(4, 4),
                         activation="relu"))
        model.add(Conv2D(64, kernel_size=(2, 2),
                         activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_last"))

        model.add(Flatten())
        model.add(Dense(512, activation="relu"))

        model.add(Dense(action_count, activation='linear'))

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.001),
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _pre_process(input_data):
        return input_data.reshape(1, RAW_WIDTH, RAW_HEIGHT, 1)


def combine_two_observations(observation, observation_next):
    grey_matrix = color.rgb2gray(observation)
    grey_matrix = transform.resize(grey_matrix, (RAW_WIDTH, RAW_HEIGHT))
    grey_matrix_next = color.rgb2gray(observation_next)
    grey_matrix_next = transform.resize(grey_matrix_next, (RAW_WIDTH, RAW_HEIGHT))
    processed_matrix = np.maximum(grey_matrix, grey_matrix_next)
    return processed_matrix


def main():
    env = gym.make("Breakout-v0")
    agent = DQNBreakout(env.action_space.n)

    for episode in range(1000000):
        observation_queue = deque(maxlen=2)
        observation = env.reset()
        observation_queue.append(observation)
        for step in range(3000):
            if len(observation_queue) >= 2:
                observation = combine_two_observations(observation_queue[0], observation_queue[1])
            else:
                observation = transform.resize(color.rgb2gray(observation), (RAW_WIDTH, RAW_HEIGHT))
            action = agent.make_action(observation)
            next_observation, reward, done, _ = env.step(action)
            agent.notify_reward(reward)
            observation_queue.append(next_observation)

            if len(observation_queue) >= 2:
                next_observation = \
                    combine_two_observations(observation_queue[0], observation_queue[1])
            else:
                next_observation = \
                    transform.resize(color.rgb2gray(observation), (RAW_WIDTH, RAW_HEIGHT))

            agent.append_memory_and_train(observation, action, reward, next_observation, done)

            observation = next_observation

            if done:
                break
        agent.episode_finished({})

if __name__ == "__main__":
    main()
