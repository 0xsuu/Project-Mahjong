#!/usr/bin/env python3

import numpy as np
import os

from multi_tile_coder import MultiTileCoder


def test1():
    dims = [2, 2]
    limits = [(0, 1), (0, 1)]

    mtc_test1 = MultiTileCoder(dims, limits, 8, 2)

    mtc_test1.tile_coders[0].tiles = np.array([1, 2, 3, 4])
    mtc_test1.tile_coders[1].tiles = np.array([5, 6, 7, 8])

    mtc_test2 = MultiTileCoder(dims, limits, 8, 2)
    mtc_test2.set_weights(mtc_test1.get_weights())

    assert np.array_equal(mtc_test2.tile_coders[0].tiles, [1, 2, 3, 4])
    assert np.array_equal(mtc_test2.tile_coders[1].tiles, [5, 6, 7, 8])

    mtc_test1.save_weights("test.h5")
    mtc_test3 = MultiTileCoder(dims, limits, 8, 2)
    mtc_test3.load_weights("test.h5")

    os.remove("test.h5")

    assert np.array_equal(mtc_test3.tile_coders[0].tiles, [1, 2, 3, 4])
    assert np.array_equal(mtc_test3.tile_coders[1].tiles, [5, 6, 7, 8])


def test2():
    dims = [2, 2]
    limits = [(0, 1), (0, 1)]

    mtc_test1 = MultiTileCoder(dims, limits, 8, 1)
    print(mtc_test1.train_on_batch(np.array([[0, 0]] * 1000), np.array([[0]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[1, 0]] * 1000), np.array([[1]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[0, 1]] * 1000), np.array([[1]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[1, 1]] * 1000), np.array([[1]] * 1000)))
    prediction = np.round(mtc_test1.predict(np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))).astype(int)
    assert np.array_equal(prediction, [[0], [1], [1], [1]])


def test3():
    dims = [2, 2]
    limits = [(0, 1), (0, 1)]

    mtc_test1 = MultiTileCoder(dims, limits, 8, 2)
    print(mtc_test1.train_on_batch(np.array([[0, 0]] * 1000), np.array([[1, 0]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[1, 0]] * 1000), np.array([[0, 2]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[0, 1]] * 1000), np.array([[0, 2]] * 1000)))
    print(mtc_test1.train_on_batch(np.array([[1, 1]] * 1000), np.array([[0, 2]] * 1000)))
    prediction = np.round(mtc_test1.predict(np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))).astype(int)
    assert np.array_equal(prediction, [[1, 0], [0, 2], [0, 2], [0, 2]])

    mtc_test2 = MultiTileCoder(dims, limits, 8, 2)
    mtc_test2.set_weights(mtc_test1.get_weights())
    prediction = np.round(mtc_test2.predict(np.array([[0, 0], [1, 0], [0, 1], [1, 1]]))).astype(int)
    assert np.array_equal(prediction, [[1, 0], [0, 2], [0, 2], [0, 2]])

if __name__ == "__main__":
    test1()
    test2()
    test3()
