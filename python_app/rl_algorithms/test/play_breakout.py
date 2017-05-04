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

from breakout_test import *

import gym


def combine_two_observations(observation, observation_next):
    grey_matrix = color.rgb2gray(observation)
    grey_matrix = transform.resize(grey_matrix, (RAW_WIDTH, RAW_HEIGHT))
    grey_matrix_next = color.rgb2gray(observation_next)
    grey_matrix_next = transform.resize(grey_matrix_next, (RAW_WIDTH, RAW_HEIGHT))
    processed_matrix = np.maximum(grey_matrix, grey_matrix_next)
    return processed_matrix


def main():
    env = gym.make("Breakout-v0")
    agent = DQNBreakout(env.action_space.n, mode=PLAY, load=True)

    total_reward = 0
    observation_queue = deque(maxlen=2)
    observation = env.reset()
    observation_queue.append(observation)
    for step in range(3000):
        # env.render()
        if len(observation_queue) >= 2:
            observation = combine_two_observations(observation_queue[0], observation_queue[1])
        else:
            observation = transform.resize(color.rgb2gray(observation), (RAW_WIDTH, RAW_HEIGHT))
        action = agent.make_action(observation)
        next_observation, reward, done, _ = env.step(action)
        total_reward += reward
        observation_queue.append(next_observation)

        if len(observation_queue) >= 2:
            next_observation = \
                combine_two_observations(observation_queue[0], observation_queue[1])
        else:
            next_observation = \
                transform.resize(color.rgb2gray(observation), (RAW_WIDTH, RAW_HEIGHT))

        observation = next_observation

        if done:
            break

    env.close()
    print("Total reward:", total_reward)

if __name__ == "__main__":
    main()
