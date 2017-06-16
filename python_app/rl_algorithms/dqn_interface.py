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

from abc import ABCMeta, abstractmethod, abstractstaticmethod
from datetime import datetime
import os

import numpy as np
import tensorflow as tf

# Mode definitions.
TRAIN = 100
PLAY = 200
EVAL = 300
DEBUG = 400
SELF_PLAY = 500

EPSILON_LOWER_BOUND = 0.0
EPSILON_UPPER_BOUND = 1.0

REPLAY_MEMORY_SIZE_DEFAULT = 10000
REPLAY_MEMORY_BATCH_SIZE_DEFAULT = 32

TRAIN_STEP_INTERVAL_DEFAULT = 4
TARGET_UPDATE_INTERVAL_DEFAULT = 100
SAVE_WEIGHTS_INTERVAL_DEFAULT = 100
SELF_PLAY_UPDATE_INTERVAL_DEFAULT = 1001
PRINT_SUMMARY_INTERVAL_DEFAULT = 100

GAMMA_DEFAULT = 0.99  # Reward discount factor.


class DQNInterface:
    __metaclass__ = ABCMeta

    def __init__(self, action_count, weights_file_path,
                 model_input_shape=None,
                 mode=TRAIN, load_previous_model=False,
                 replay_memory_size=REPLAY_MEMORY_SIZE_DEFAULT,
                 replay_memory_batch_size=REPLAY_MEMORY_BATCH_SIZE_DEFAULT,
                 train_step_interval=TRAIN_STEP_INTERVAL_DEFAULT,
                 target_update_interval=TARGET_UPDATE_INTERVAL_DEFAULT,
                 gamma=GAMMA_DEFAULT,
                 initial_epsilon=1.0, final_epsilon=0.01, epsilon_decay_steps=10000):
        self._mode = mode
        self._action_count = action_count
        self._weights_file_path = weights_file_path

        # Initialising Q functions.
        # Online model.
        self._model = self._create_model(model_input_shape, action_count)
        # Target model.
        self._target_model = self._create_model(model_input_shape, action_count)
        self._target_model.set_weights(self._model.get_weights())  # Copy weights.
        self._target_update_interval = target_update_interval

        self._replay_memory = self._create_replay_memory(replay_memory_size)
        self._replay_memory_batch_size = replay_memory_batch_size
        self._train_step_interval = train_step_interval

        # Setup epsilon.
        self._final_epsilon = final_epsilon
        self._epsilon_decay_value = (initial_epsilon - final_epsilon) / epsilon_decay_steps
        self._epsilon = initial_epsilon

        # Setup gamma.
        self._gamma = gamma

        # Milestone variables.
        self._timestamp = 0
        self._timestamp_in_episode = 0
        self._episode = 0

        # Episode-wised status variables.
        self._max_q_history = []
        self._total_reward = 0
        self._losses = []

        # Period-wised status variables.
        self._period_max_q_histories = []
        self._period_total_rewards = []

        # Load.
        if load_previous_model:
            self.load_previous_run()

        if self._mode == TRAIN:
            self._writer = self.setup_tensorboard_writer()

        # Print info.
        print("Mode:", mode,
              "| Replay memory size:", replay_memory_size,
              "| Train step interval:", train_step_interval,
              "| Target update interval:", target_update_interval)

    @staticmethod
    @abstractstaticmethod
    def _create_replay_memory(max_size=None):
        raise Exception("Do not call abstract method.")

    @abstractmethod
    def _train_on_memory(self, observation_batch,
                         action_batch,
                         reward_batch,
                         observation_next_batch,
                         done_batch,
                         weights=None,
                         batch_indexes=None):
        raise Exception("Do not call abstract method.")

    @abstractmethod
    def _sample_replay_memory(self):
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _create_model(input_shape=None, action_count=None):
        raise Exception("Do not call abstract method.")

    @staticmethod
    @abstractstaticmethod
    def _pre_process(input_data):
        raise Exception("Do not call abstract method.")

    def append_memory_and_train(self, observation, action, reward, observation_next, done):
        assert self._mode == TRAIN

        self._replay_memory.append((self._pre_process(observation),
                                    action,
                                    reward,
                                    self._pre_process(observation_next),
                                    done))

        if len(self._replay_memory) > self._replay_memory_batch_size and \
           self._timestamp % self._train_step_interval == 0:
            # Sample the mini batch.
            environment = self._sample_replay_memory()
            if len(environment) == 5:
                # Queue memory.
                observation_batch, \
                  action_batch, \
                  reward_batch, \
                  observation_next_batch, \
                  done_batch = environment
                weights = None
                batch_indexes = None
            elif len(environment) == 7:
                # Prioritised memory.
                observation_batch, \
                  action_batch, \
                  reward_batch, \
                  observation_next_batch, \
                  done_batch, \
                  weights, \
                  batch_indexes = environment
            else:
                raise Exception("Unexpected number of returns from _sample_replay_memory()!")
            # Observations must be in the shape of (1, ...).
            # This should be handled in _pre_process function.
            self._train_on_memory(observation_batch,
                                  action_batch,
                                  reward_batch,
                                  observation_next_batch,
                                  done_batch,
                                  weights,
                                  batch_indexes)
            if self._timestamp % self._target_update_interval == 0:
                self._target_model.set_weights(self._model.get_weights())

    def make_action(self, observation, mode=None):
        if mode is None:
            backup_mode = None
            mode = self._mode
        else:
            backup_mode = self._mode
            self._mode = mode
        if mode == TRAIN:
            choice = self._epsilon_greedy_choose(self._pre_process(observation))
            if self._epsilon > self._final_epsilon:
                self._epsilon -= self._epsilon_decay_value
        else:
            choice = self._max_q_choose(self._pre_process(observation))
        if backup_mode:
            self._mode = backup_mode
        return choice

    def notify_reward(self, reward):
        self._total_reward += reward

    def _epsilon_greedy_choose(self, input_data):
        """
        This function should ideally be used only under TRAIN mode.

        :param input_data: the pre-processed data to feed into the neural network.
        :return: The index(action) selected following epsilon greedy strategy.
        """
        self._timestamp += 1
        q_values = self._model.predict(input_data)[0]
        self._max_q_history.append(np.max(q_values))

        if np.random.uniform(EPSILON_LOWER_BOUND, EPSILON_UPPER_BOUND) < self._epsilon:
            return np.random.randint(0, self._action_count)  # Range is [0, self._action_count).
        else:
            # Choose the maximum Q's index as a policy.
            return np.argmax(q_values)

    def _max_q_choose(self, input_data):
        q_values = self._model.predict(input_data)[0]
        choice = np.argmax(q_values)
        if self._mode == DEBUG:
            print("Q values:", q_values)
            print("Choice:", choice)
            print()
        return choice

    def load_previous_run(self):
        if os.path.isfile(self._weights_file_path):
            print(self._weights_file_path, "loaded.")
            self._model.load_weights(self._weights_file_path)
            self._target_model.set_weights(self._model.get_weights())  # Copy weights.

    @staticmethod
    def setup_tensorboard_writer(title=str(datetime.now())):
        return tf.summary.FileWriter("./logs/" + title)

    def episode_finished(self, additional_logs):
        self._episode += 1
        if self._mode == TRAIN:
            summary = tf.Summary()
            if len(self._max_q_history) > 0:
                average_max_q = sum(self._max_q_history) / len(self._max_q_history)
                summary.value.add(tag="Average Max Q", simple_value=average_max_q)
            if len(self._losses) > 0:
                average_loss = sum(self._losses) / len(self._losses)
                summary.value.add(tag="Average Loss", simple_value=average_loss)

            summary.value.add(tag="Total Reward", simple_value=self._total_reward)
            for tag in additional_logs:
                summary.value.add(tag=tag, simple_value=additional_logs[tag])

            # Append periodical data.
            self._period_max_q_histories += self._max_q_history
            self._period_total_rewards.append(self._total_reward)

            # Periodical report.
            if self._episode % PRINT_SUMMARY_INTERVAL_DEFAULT == 0:
                if len(self._period_max_q_histories) > 0:
                    period_average_max_q = \
                        sum(self._period_max_q_histories) / len(self._period_max_q_histories)
                else:
                    period_average_max_q = 0
                period_average_total_reward = \
                    sum(self._period_total_rewards) / len(self._period_total_rewards)
                tag_max_qs = "Average max Q over " + \
                             str(PRINT_SUMMARY_INTERVAL_DEFAULT) + " episodes"
                tag_rewards = "Average Total reward over " + \
                              str(PRINT_SUMMARY_INTERVAL_DEFAULT) + " episodes"
                print("Epsilon:", self._epsilon, "\t",
                      tag_max_qs + ":",
                      period_average_max_q, "\t",
                      tag_rewards + ":",
                      period_average_total_reward)
                summary.value.add(tag=tag_max_qs, simple_value=period_average_max_q)
                summary.value.add(
                    tag=tag_rewards,
                    simple_value=period_average_total_reward)
                self._period_max_q_histories = []
                self._period_total_rewards = []

            # Reset status variables.
            self._max_q_history = []
            self._total_reward = 0

            self._writer.add_summary(summary, self._episode)
            self._writer.flush()

            # Save weights.
            if self._episode % SAVE_WEIGHTS_INTERVAL_DEFAULT == 0:
                print("Finished", self._episode, "episodes.")
                self._model.save_weights(self._weights_file_path)
        elif self._mode == SELF_PLAY:
            if self._episode % SELF_PLAY_UPDATE_INTERVAL_DEFAULT == 0:
                print("Updated to the newest model.")
                self._model.load_weights(self._weights_file_path)
