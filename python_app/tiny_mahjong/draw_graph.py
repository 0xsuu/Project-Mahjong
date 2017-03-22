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

import matplotlib.pylab as plt
import numpy as np


def main():
    values = np.loadtxt("mc_values.txt")
    figures = values[:, 0]
    indexes = np.arange(len(figures))
    plt.bar(indexes + 0.1, figures)
    plt.title("State Frequency Histogram")
    plt.xlabel("State NO.")
    plt.ylabel("Frequency")

    plt.show()

if __name__ == "__main__":
    main()
