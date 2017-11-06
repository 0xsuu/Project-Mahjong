#!/usr/bin/env python3

# -*- coding: utf-8 -*-

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


import numpy as np
import numpy.random as random

from game_state import GameState

__version__ = "0.2b"

TILE_SET = np.array(
    [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3,
        4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6,
        7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9,
        10, 10, 10, 10, 11, 11, 11, 11,
        12, 12, 12, 12, 13, 13, 13, 13,
        14, 14, 14, 14, 15, 15, 15, 15,
        16, 16, 16, 16, 17, 17, 17, 17,
        18, 18, 18, 18])

WIN = 6666
DISCARD = 1111
PASS = 2222


class Player:
    def __init__(self, name):
        assert name != ""
        self.name = name
        self.hand = np.array([])
        self.turn_count = 0
        self.average_turn = 0
        self.rounds_won = 0
        self.rounds_lost = 0
        self.__game = None
        self._temporary_removed_tile = None
        self.game_state = None

    def initial_hand_obtained(self):
        assert len(self.hand) == 4
        self.turn_count = 0

    def tile_picked(self):
        """
        This method should return an action of Win or Discard,
        and the index of the tile in player's hand to discard if the action is Discard.
        """
        assert len(self.hand) == 5
        self.turn_count += 1

    def player_discarded(self, discarded_tile):
        if self.test_win_hand(self.hand, discarded_tile):
            return WIN
        else:
            return PASS

    def game_ends(self, win, lose, self_win=False, drain=False):
        if win:
            self.rounds_won += 1
            self.average_turn += 1/self.rounds_won * (self.turn_count - self.average_turn)
        if lose and not self_win:
            self.rounds_lost += 1

    @staticmethod
    def test_win_hand(hand, tile=None):
        if tile is not None:
            hand = np.append(hand, tile)
            hand = np.sort(hand)
        for i in range(len(hand)-1):
            if hand[i] == hand[i+1]:
                copy_hand = np.copy(hand)
                copy_hand = np.delete(copy_hand, [i, i+1])
                if (copy_hand[0] <= 9 and copy_hand[1] <= 9 and copy_hand[2] <= 9) or \
                        (copy_hand[0] > 9 and copy_hand[1] > 9 and copy_hand[2] > 9):
                    if (copy_hand[0] == copy_hand[1] and copy_hand[1] == copy_hand[2]) or \
                            (copy_hand[0] == copy_hand[1]-1 and copy_hand[1] == copy_hand[2]-1):
                                return True
        return False

    def test_win(self):
        return self.test_win_hand(self.hand)

    def insert(self, tile):
        self.hand = np.append(self.hand, tile)
        self.sort_hand()

    def sort_hand(self):
        self.hand = np.sort(self.hand)

    def set_game(self, game):
        self.__game = game

    def has_tile_in_stack(self, tile):
        return len(np.argwhere(self.__game.tiles == tile))

    def get_remaining_tiles(self):
        return len(self.__game.tiles)

    def get_pick_tile_probability(self, tile):
        if self.get_remaining_tiles() != 0:
            return self.has_tile_in_stack(tile) / self.get_remaining_tiles()
        else:
            return 0

    def temporary_remove_tile_from_stack(self, tile):
        self._temporary_removed_tile = tile
        if len(np.argwhere(self.__game.tiles == tile)) > 0:
            self.__game.tiles = \
                np.delete(self.__game.tiles, np.argwhere(self.__game.tiles == tile)[0])

    def restore_temporary_removed_tile(self):
        self.__game.tiles = np.append(self.__game.tiles, self._temporary_removed_tile)
        self.__game.tiles.sort()
        self._temporary_removed_tile = None


class Game:
    def __init__(self, round_count, players, win_on_discard, disclose_all=False):
        self.players = players
        self.round_count = round_count
        self.current_round = 0
        self.tiles = None
        self.current_player = None
        self.win_on_discard = win_on_discard
        self._disclose_all = disclose_all

    def setup(self):
        self.tiles = np.copy(TILE_SET)
        np.random.shuffle(self.tiles)
        self.current_player = random.choice(self.players)

        for player in self.players:
            player.set_game(self)
            player.hand = np.array([])
        for i in range(4):
            for player in self.players:
                player.hand = np.append(player.hand, self.tiles[0])
                self.tiles = np.delete(self.tiles, 0)
        for player in self.players:
            # Generate game states for players.
            other_players = self.players[:]
            other_players.remove(player)
            player.game_state = GameState(other_players, disclose_all=self._disclose_all)

            player.sort_hand()
            player.game_state.on_player_default_hand_obtained(np.copy(player.hand))

            player.initial_hand_obtained()

        if self._disclose_all:
            for target in self.players:
                hands = np.array([])
                for objective in self.players:
                    if target != objective:
                        hands = np.append(hands, np.append(objective.hand, 0))
                target.game_state.on_other_players_hands_obtained(hands)

    def _next_player(self):
        index = self.players.index(self.current_player) + 1
        if index >= len(self.players):
            index = 0
        return self.players[index]

    def play_round(self):
        self.setup()
        while True:
            # Current player draws tile.
            self.current_player.insert(self.tiles[0])

            # Update hand in Game State for current player.
            self.current_player.game_state.on_player_pick_new_tile(np.copy(self.current_player.hand))

            # Update opponents hands in Game State for all other players.
            if self._disclose_all:
                for target in self.players:
                    hands = np.array([])
                    for objective in self.players:
                        if target != objective:
                            if objective.hand.shape[0] == 4:
                                hands = np.append(hands, np.append(objective.hand, 0))
                            else:
                                hands = np.append(hands, objective.hand)
                    target.game_state.on_other_players_hands_obtained(hands)

            self.tiles = np.delete(self.tiles, 0)

            # Get current player's action (and discarded tile's index).
            action, index = self.current_player.tile_picked()

            if action == WIN:
                # Self-Win.
                self._delete_tile_and_notify(index)
                # Notify all the players the game result.
                for player in self.players:
                    if player == self.current_player:
                        player.game_ends(True, False, self_win=True)
                    else:
                        player.game_ends(False, True, self_win=True)
                return self.current_player.name
            elif action == DISCARD:
                discarded_tile = self._delete_tile_and_notify(index)
                # Notify all the other players of the discard.
                if self.win_on_discard:
                    for discard_react_player in self.players:
                        # Skip current player.
                        if discard_react_player is not self.current_player:
                            action = discard_react_player.player_discarded(discarded_tile)
                            if action == WIN:
                                # Notify all the players the game result.
                                for player_to_notify in self.players:
                                    if player_to_notify == discard_react_player:
                                        # Win player.
                                        player_to_notify.game_ends(True, False)
                                    elif player_to_notify == self.current_player:
                                        # Lose player.
                                        player_to_notify.game_ends(False, True)
                                    else:
                                        # Non of the rest players business.
                                        player_to_notify.game_ends(False, False)
                                return discard_react_player.name
            else:
                raise ValueError("Unknown action")

            if len(self.tiles) == 0:
                # Notify all the players the game has drained.
                for player in self.players:
                    player.game_ends(False, False, drain=True)
                return ""
            else:
                self.current_player = self._next_player()

    def _delete_tile_and_notify(self, index):
        discarded_tile = self.current_player.hand[index]
        hand_with_zero = self.current_player.hand.copy()
        # hand_with_zero[index] = 0
        self.current_player.hand = \
            np.delete(self.current_player.hand, index)
        for p in self.players:
            # TODO: Add a player list to improve efficiency.
            if p == self.current_player:
                p.game_state.on_player_discard(discarded_tile,
                                               hand_with_zero)
            else:
                p.game_state.on_other_player_discard(player_id=self.current_player,
                                                     tile=discarded_tile,
                                                     new_hand=hand_with_zero)
        return discarded_tile

    def play(self):
        counter = {"": 0}
        for player in self.players:
            counter[player.name] = 0
        for i in range(self.round_count):
            # print("Current Round:", self.current_round)
            counter[self.play_round()] += 1
            self.current_round += 1
        for player in self.players:
            print(player.name + "'s win rate: " +
                  str(counter[player.name] / self.round_count * 100) + "%" +
                  ", lose rate: " + str(player.rounds_lost * 100 / self.round_count) + "%" +
                  ", average turn to win: " + str(player.average_turn))
        print("Drain rate: " + str(counter[""] * 100.0 / self.round_count) + "%")

