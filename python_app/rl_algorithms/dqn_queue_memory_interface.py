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

from dqn_interface import *

from collections import deque
from random import sample


class DQNQueueMemoryInterface(DQNInterface):
    __metaclass__ = ABCMeta

    @staticmethod
    def _create_replay_memory(max_size=None):
        return deque(maxlen=max_size)

    def _sample_replay_memory(self):
        mini_batch = sample(list(self._replay_memory), self._replay_memory_batch_size)
        observation_batch = np.array([m[0][0] for m in mini_batch])
        action_batch = [m[1] for m in mini_batch]
        reward_batch = [m[2] for m in mini_batch]
        observation_next_batch = np.array([m[3][0] for m in mini_batch])
        done_batch = [m[4] for m in mini_batch]
        return observation_batch, action_batch, reward_batch, observation_next_batch, done_batch

    @abstractmethod
    def _train_on_memory(self, observation_batch,
                         action_batch,
                         reward_batch,
                         observation_next_batch,
                         done_batch,
                         weights=None,
                         batch_indexes=None):
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _create_model(input_shape=None, action_count=None):
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _pre_process(input_data):
        raise Exception("Do not call abstract method.")
