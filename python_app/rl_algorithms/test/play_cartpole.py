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

from dqn_cartpole import *

import gym


def main():
    env = gym.make("CartPole-v0")
    agent = DQNCartpole(env.action_space.n, mode=PLAY, load=True)

    total_reward = 0
    observation = env.reset()
    for step in range(300):
        env.render()
        action = agent.make_action(observation)
        observation, reward, done, _ = env.step(action)
        total_reward += reward

        if done:
            break

    env.close()
    print("Total reward:", total_reward)

if __name__ == "__main__":
    main()
