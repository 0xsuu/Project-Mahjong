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

import h5py
from math import sqrt
import numpy as np

SAVER_WEIGHTS_KEY = "tile_coding_tiles"


class MultiTileCoder:
    def __init__(self, dims, limits, tilings, output_number, step_size=0.1, offset=lambda n: 2 * np.arange(n) + 1):
        self._output_numbers = output_number
        self.tile_coders = []
        for i in range(output_number):
            self.tile_coders.append(TileCoder(dims, limits, tilings, step_size, offset))

    def predict(self, input_data):
        predictions = np.zeros((input_data.shape[0], self._output_numbers))
        for i in range(input_data.shape[0]):
            single_prediction = []
            for t in self.tile_coders:
                single_prediction.append(t[input_data[i]])
            predictions[i] = single_prediction
        return predictions

    def train_on_batch(self, Xs, Ys):
        total_loss = 0
        for i in range(Xs.shape[0]):
            for j in range(self._output_numbers):
                total_loss += sqrt((Ys[i][j] - self.tile_coders[j][Xs[i]]) ** 2)
                self.tile_coders[j][Xs[i]] = Ys[i][j]
        return total_loss

    def get_weights(self):
        return self

    def set_weights(self, weights):
        for i in range(len(self.tile_coders)):
            self.tile_coders[i].tiles = weights.tile_coders[i].tiles[:]

    def save_weights(self, file_path):
        h5_file = h5py.File(file_path, "w")
        for i in range(len(self.tile_coders)):
            h5_file.create_dataset(SAVER_WEIGHTS_KEY + str(i), data=self.tile_coders[i].tiles)
        h5_file.close()

    def load_weights(self, file_path):
        h5_file = h5py.File(file_path, "r")
        current_index = 0
        while SAVER_WEIGHTS_KEY + str(current_index) in h5_file:
            self.tile_coders[current_index].tiles = h5_file[SAVER_WEIGHTS_KEY + str(current_index)][:]
            current_index += 1
        h5_file.close()


class TileCoder:
    def __init__(self, dims, limits, tilings, step_size=0.1, offset=lambda n: 2 * np.arange(n) + 1):
        offset_vec = offset(len(dims))
        tiling_dims = np.array(dims, dtype=np.int) + offset_vec
        self._offsets = offset_vec * np.repeat([np.arange(tilings)], len(dims), 0).T / float(tilings)
        self._limits = np.array(limits)
        self._norm_dims = np.array(dims) / (self._limits[:, 1] - self._limits[:, 0])
        self._alpha = step_size / tilings
        self.tiles = np.zeros(tilings * np.prod(tiling_dims))
        self._tile_base_ind = np.prod(tiling_dims) * np.arange(tilings)
        self._hash_vec = np.ones(len(dims), dtype=np.int)
        for i in range(len(dims) - 1):
            self._hash_vec[i + 1] = tiling_dims[i] * self._hash_vec[i]

    def _get_tiles(self, x):
        off_coordinates = ((x - self._limits[:, 0]) * self._norm_dims + self._offsets).astype(int)
        return self._tile_base_ind + np.dot(off_coordinates, self._hash_vec)

    def __getitem__(self, x):
        tile_ind = self._get_tiles(x)
        return np.sum(self.tiles[tile_ind])

    def __setitem__(self, x, val):
        tile_ind = self._get_tiles(x)
        self.tiles[tile_ind] += self._alpha * (val - np.sum(self.tiles[tile_ind]))