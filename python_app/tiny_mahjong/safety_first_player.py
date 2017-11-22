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

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

from collections import deque
from random import sample

from dqn_interface import *

from game import *

from utils.combination_calculator import get_combinations

Q_VALUES_FILE = "q_values.txt"
ALL_COMBINATIONS = get_combinations()

SL_MODEL_WEIGHTS_FILE = "tm_safety_sl_weights.h5"
SAVE_WEIGHT_INTERVAL = 2000

TRAIN_STEP_INTERVAL = 4
MINI_BATCH_SIZE = 256
MEMORY_MAX_LEN = 5000000

HAND_SIZE = 5

# Input features: probability of 18 types of tiles of unrevealed tiles +
#                 remaining tiles + A/B ratio + opponent last 5 discards.
STATE_SIZE = 18 + 1 + 2 + 5
OUTPUT_SIZE = 18


class ReplayMemory:
    def __init__(self, max_len):
        self.__memory = deque(maxlen=max_len)

    def sample(self, sample_size=MINI_BATCH_SIZE):
        mini_batch = sample(list(self.__memory), sample_size)
        input_batch = np.array([m[0] for m in mini_batch])
        label_batch = np.array([m[1] for m in mini_batch])
        return input_batch, label_batch

    def append(self, input_data, label_data):
        self.__memory.append((input_data, label_data))

    def get_len(self):
        return len(self.__memory)


class SafetyFirstPlayer(Player):
    def __init__(self, name, mode, log_game_state=False):
        Player.__init__(self, name, log_game_state)
        self._mode = mode

        if os.path.isfile(Q_VALUES_FILE):
            self.q_values = np.loadtxt(Q_VALUES_FILE)
        else:
            raise FileNotFoundError("No Q values file present.")
        self._sl_model = SafetyFirstPlayer.build_model()
        if os.path.isfile(SL_MODEL_WEIGHTS_FILE):
            self._sl_model.load_weights(SL_MODEL_WEIGHTS_FILE)
            print(SL_MODEL_WEIGHTS_FILE, "loaded.")
        self._replay_memory = ReplayMemory(MEMORY_MAX_LEN)

        self._drain_rounds = 0
        self._total_rounds = 0
        self._steps = 0

        if self._mode == TRAIN:
            self._tensorboard_writer = tf.summary.FileWriter("./logs/" + str(datetime.now()))
        else:
            self._tensorboard_writer = None

        self._average_loss = 0.0
        self._average_accuracy = 0.0
        self._metrics_counter = 0

    @staticmethod
    def build_model():
        model = Sequential()
        model.add(Dense(64, input_shape=(STATE_SIZE,), activation="relu"))
        model.add(Dense(32, activation="relu"))
        model.add(Dense(OUTPUT_SIZE, activation="sigmoid"))

        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.00025),
                      metrics=['accuracy'])

        return model

    def initial_hand_obtained(self):
        Player.initial_hand_obtained(self)

        self._average_loss = 0.0
        self._average_accuracy = 0.0
        self._metrics_counter = 0

        self._total_rounds += 1

    def tile_picked(self):
        Player.tile_picked(self)
        if self.test_win():
            return WIN, -1
        else:
            processed_input = np.array(self.game_state.process_dangerousness_input())
            if processed_input.shape[0] == 0:
                tile_dangerousness_distribution = [0.0] * 18
            else:
                tile_dangerousness_distribution = \
                    self._sl_model.predict(processed_input.reshape(1, processed_input.shape[0]))[0]
            hand_dangerousness = []
            for i in self.hand:
                hand_dangerousness.append(tile_dangerousness_distribution[int(i) - 1])

            # q_values = self.q_values[ALL_COMBINATIONS.index(self.hand.tolist())]
            # for i in range(5):
            #     q_values[i] -= hand_dangerousness[i] * 8
            # action = np.argmax(q_values)

            action = np.argmin(hand_dangerousness)

            if self._mode == DEBUG:
                print(self.name)
                print("Hand:")
                print(self.hand)
                print("Hand Dangerousness:")
                print(hand_dangerousness)
                # print("Modified Q values:")
                # print(q_values)
                print("Discard:", action)
                print("Input:")
                print(processed_input)
                print("All Tiles Dangerousness:")
                print(tile_dangerousness_distribution)
                print()
            return DISCARD, action

    def player_discarded(self, discarded_tile):
        self._steps += 1
        if self._mode == TRAIN:
            processed_inputs = self.game_state.process_dangerousness_input()
            processed_labels = [0] * OUTPUT_SIZE

            # Process labels.
            for i in self.game_state.calc_shanten_tenpai_tiles(self.game_state.get_opponents_hands())[2]:
                processed_labels[i - 1] = 1

            assert len(processed_inputs) == STATE_SIZE
            self._replay_memory.append(processed_inputs, processed_labels)

            if self._replay_memory.get_len() > MINI_BATCH_SIZE and self._steps % TRAIN_STEP_INTERVAL == 0:
                inputs, labels = self._replay_memory.sample()
                train_metrics = self._sl_model.train_on_batch(inputs, labels)
                self._average_loss += train_metrics[0]
                self._average_accuracy += train_metrics[1]
                self._metrics_counter += 1

        if self.test_win_hand(self.hand, discarded_tile):
            return WIN
        else:
            return PASS

    def game_ends(self, win, lose, self_win=False, drain=False):
        Player.game_ends(self, win, lose, self_win, drain)

        # Summary.
        if drain:
            self._drain_rounds += 1

        if self._mode == TRAIN:
            summary = tf.Summary()
            summary.value.add(tag="Win rate", simple_value=self.rounds_won * 1.0 / self._total_rounds)
            summary.value.add(tag="Lose rate", simple_value=self.rounds_lost * 1.0 / self._total_rounds)
            summary.value.add(tag="Drain rate", simple_value=self._drain_rounds * 1.0 / self._total_rounds)
            if self._metrics_counter != 0:
                summary.value.add(tag="Average loss", simple_value=self._average_loss / self._metrics_counter)
                summary.value.add(tag="Average accuracy", simple_value=self._average_accuracy / self._metrics_counter)

            self._tensorboard_writer.add_summary(summary, self._total_rounds)
            self._tensorboard_writer.flush()

            if self._total_rounds % SAVE_WEIGHT_INTERVAL == 0:
                print("Win rate:", self.rounds_won * 1.0 / self._total_rounds,
                      "\t\t\t| Lose rate:", self.rounds_lost * 1.0 / self._total_rounds,
                      "\t\t\t| Drain rate:", self._drain_rounds * 1.0 / self._total_rounds)
                self._sl_model.save_weights(SL_MODEL_WEIGHTS_FILE)

        if self._mode == PLAY:
            print(self.name + ":")
            if win:
                print("Won!")
        elif self._mode == EVAL:
            print(self.name + ":")
            print("Win rate:", str(self.rounds_won * 100.0 / self._total_rounds) + "%, Lose rate:",
                  str(self.rounds_lost * 100.0 / self._total_rounds) + "%")
        elif self._mode == DEBUG:
            if win:
                if self_win:
                    print(self.name, "self win!")
                else:
                    print(self.name, "win on discard!")
            elif lose:
                if self_win:
                    print(self.name, "lose, opponent self win.")
                else:
                    print(self.name, "lose, opponent win on this discard.")
            else:
                print("Tile stack drained.")

            print()
            print()
            print()
