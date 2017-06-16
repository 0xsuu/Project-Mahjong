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
from prioritised_double_dqn import *

from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import Adam

import gym
from gym_gomoku.envs import GomokuEnv

RAW_WIDTH = 9
RAW_HEIGHT = 9


class DQNGomoku(PrioritisedDoubleDQN):
    def __init__(self, action_count, weights_file_path="gomoku_weights.h5", mode=TRAIN):
        PrioritisedDoubleDQN.__init__(self, action_count, weights_file_path,
                                      replay_memory_size=100000,
                                      target_update_interval=1000, gamma=0.99,
                                      load_previous_model=True, mode=mode)

    @staticmethod
    def _create_model(input_shape=None, action_count=None):
        model = Sequential()
        model.add(Conv2D(32, kernel_size=(3, 3), padding="same", strides=(2, 2),
                         input_shape=(RAW_WIDTH, RAW_HEIGHT, 1),
                         activation="relu", kernel_initializer="random_normal"))
        model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1),
                         activation="relu"))
        model.add(Conv2D(64, kernel_size=(2, 2),
                         activation="relu"))

        model.add(Flatten())
        model.add(Dense(512, activation="relu"))

        model.add(Dense(action_count, activation='linear'))

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.00025),
                      metrics=['accuracy'])

        return model

    @staticmethod
    def _pre_process(input_data):
        return input_data.reshape(1, RAW_WIDTH, RAW_HEIGHT, 1)


def main():
    env = GomokuEnv("black", "beginner", 9)
    agent = DQNGomoku(env.action_space.n)

    win_rate = 0.0
    for episode in range(1000000):
        observation = env.reset()
        successful_moves = 0
        for step in range(81):
            action = agent.make_action(observation)
            try:
                next_observation, reward, done, _ = env.step(action)
            except gym.error.Error:
                reward = -1
                done = True
            successful_moves += 1
            if not done:
                reward = 0.01
            else:
                if reward > 0:
                    win_rate = (win_rate * float(episode) + 1) / (episode + 1)
                else:
                    win_rate = (win_rate * float(episode)) / (episode + 1)
            agent.notify_reward(reward)

            agent.append_memory_and_train(observation, action, reward, next_observation, done)

            observation = next_observation

            if done:
                break
        agent.episode_finished({"Successful moves": successful_moves, "Win rate": win_rate})

if __name__ == "__main__":
    main()
