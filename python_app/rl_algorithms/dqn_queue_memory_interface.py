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
    def _create_replay_memory():
        return deque()

    def _discard_overflow_memory(self):
        self._replay_memory = self._replay_memory.popleft()

    def _sample_replay_memory(self):
        return sample(list(self._replay_memory), self._replay_memory_batch_size)

    @abstractmethod
    def _train_on_memory(self, mini_batch):
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _create_model():
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _pre_process(input_data):
        raise Exception("Do not call abstract method.")
