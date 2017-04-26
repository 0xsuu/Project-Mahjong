#!/usr/bin/env python3

import numpy as np


def tile_to_byte(t):
    if t[0].isdigit():
        t_value = int(t[0])
    else:
        # Avoiding White Dragon & West Wind, so change to Bai Dragon.
        if t[1] == "d" and t[0] == "w":
            t_value = 6
        else:
            t_value = {"e": 1, "s": 2, "w": 3, "n": 4, "r": 5, "b": 6, "g": 7}[t[0]]
    t_type = {"m": 0, "p": 1, "s": 2, "w": 3, "d": 3}[t[1]]
    t_meld = 0
    if len(t) > 2:
        t_meld = int(t[2])
    return t_meld << 6 | t_type << 4 | t_value


def byte_to_tile(b):
    types = ["m", "p", "s", "z"]
    return str(b & 0b1111) + types[(b & 0b110000) >> 4]


def to_mahjong_hand(hand):
    ret_hand = []
    for i in hand:
        ret_hand.append(tile_to_byte(i))
    ret_hand.sort()
    return ret_hand


def to_string_hand(hand):
    ret_hand = []
    for i in hand:
        ret_hand.append(byte_to_tile(i))
    return " ".join(ret_hand)


def transform_hand_to_one_hot(byte_hand):
    ret_hand = []
    for i in byte_hand:
        if type(i).__name__ == "Tile":
            i = i.get_data()
        # Convert to one-hot encoding.
        converted_hand = 1 << (2 - ((i & 0b11000000) >> 6))
        converted_hand <<= 13
        converted_hand |= 1 << (3 - ((i & 0b110000) >> 4) + 9)
        converted_hand |= 1 << (9 - (i & 0b1111))
        ret_hand += list(bin(converted_hand)[2:].zfill(16))
    return ret_hand


def transform_one_hot_to_cnn_matrix(csv_hand):
    csv_hand = np.array([csv_hand])
    return csv_hand.reshape(csv_hand.shape[0], 14, 16, 1)
