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

from third_party.replay_buffer import PrioritizedReplayBuffer

prioritised_memory_alpha = 0.6


class DQNPrioritisedMemoryInterface(DQNInterface):
    __metaclass__ = ABCMeta

    def __init__(self, action_count, weights_file_path, prioritised_beta_initial=0.4,
                 prioritised_beta_update_interval=100000,
                 model_input_shape=None,
                 mode=TRAIN, load_previous_model=False,
                 replay_memory_size=REPLAY_MEMORY_SIZE_DEFAULT,
                 replay_memory_batch_size=REPLAY_MEMORY_BATCH_SIZE_DEFAULT,
                 train_step_interval=TRAIN_STEP_INTERVAL_DEFAULT,
                 target_update_interval=TARGET_UPDATE_INTERVAL_DEFAULT,
                 gamma=GAMMA_DEFAULT,
                 initial_epsilon=1.0, final_epsilon=0.01, epsilon_decay_steps=10000):
        DQNInterface.__init__(self, action_count, weights_file_path,
                              model_input_shape,
                              mode, load_previous_model,
                              replay_memory_size,
                              replay_memory_batch_size,
                              train_step_interval,
                              target_update_interval,
                              gamma,
                              initial_epsilon, final_epsilon, epsilon_decay_steps)
        self._prioritised_memory_beta_initial = prioritised_beta_initial
        self._prioritised_memory_beta_update_amount = \
            (1 - prioritised_beta_initial) / prioritised_beta_update_interval
        self._prioritised_beta = self._prioritised_memory_beta_initial

    @staticmethod
    def _create_replay_memory(max_size=None):
        return PrioritizedReplayBuffer(max_size, alpha=prioritised_memory_alpha)

    def _sample_replay_memory(self):
        if self._prioritised_beta < 1.0:
            self._prioritised_beta += self._prioritised_memory_beta_update_amount
        return self._replay_memory.sample(self._replay_memory_batch_size,
                                          beta=self._prioritised_beta)

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
