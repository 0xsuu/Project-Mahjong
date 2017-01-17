# -*- coding: utf-8 -*-
import logging
import random

from mahjong.constants import EAST, SOUTH, WEST, NORTH
from utils.settings_handler import settings
from mahjong.ai.shanten import Shanten
from mahjong.tile import Tile

logger = logging.getLogger('tenhou')

class Player(object):
    # the place where is player is sitting
    # always = 0 for our player
    seat = 0
    # where is sitting dealer, based on this information we can calculate player wind
    dealer_seat = 0
    # position based on scores
    position = 0
    scores = 0
    uma = 0

    name = ''
    rank = ''

    discards = []
    # tiles that were discarded after player's riichi
    safe_tiles = []
    tiles = []
    melds = []
    table = None
    in_tempai = False
    in_riichi = False
    in_defence_mode = False

    def __init__(self, seat, dealer_seat, table, use_previous_ai_version=False):
        self.discards = []
        self.melds = []
        self.tiles = []
        self.safe_tiles = []
        self.seat = seat
        self.table = table
        self.dealer_seat = dealer_seat

        if use_previous_ai_version:
            try:
                from mahjong.ai.old_version import MainAI
            # project wasn't set up properly
            # we don't have old version
            except ImportError:
                logger.error('Wasn\'t able to load old api version')
                from mahjong.ai.main import MainAI
        else:
            if settings.ENABLE_AI:
                from mahjong.ai.main import MainAI
            else:
                from mahjong.ai.random import MainAI

        from mahjong.myAI.SLCNNPlayer import SLCNNPlayer
        from mahjong.myAI.GreedyPlayer import GreedyAII
        #self.ai = random.choice([MainAI(table, self), SLCNNPlayer(table, self)])
        self.ai = SLCNNPlayer(table, self)
        #self.ai = GreedyAII(table, self)
        #from time import sleep
        #sleep(4)
        #self.ai = MainAI(table, self)

    def __str__(self):
        result = u'{0}'.format(self.name)
        if self.scores:
            result += u' ({:,d})'.format(int(self.scores))
            if self.uma:
                result += u' {0}'.format(self.uma)
        else:
            result += u' ({0})'.format(self.rank)
        return result

    # for calls in array
    def __repr__(self):
        return self.__str__()

    def add_meld(self, meld):
        self.melds.append(meld)

    def add_discarded_tile(self, tile):
        self.discards.append(Tile(tile))

    def init_hand(self, tiles):
        self.tiles = [Tile(i) for i in tiles]

    def draw_tile(self, tile):
        self.tiles.append(Tile(tile))
        # we need sort it to have a better string presentation
        self.tiles = sorted(self.tiles)

    def discard_tile(self):
        tile_to_discard = self.ai.discard_tile()
        if tile_to_discard != Shanten.AGARI_STATE:
            self.add_discarded_tile(tile_to_discard)
            self.tiles.remove(tile_to_discard)
        return tile_to_discard

    def erase_state(self):
        self.discards = []
        self.melds = []
        self.tiles = []
        self.safe_tiles = []
        self.in_tempai = False
        self.in_riichi = False
        self.in_defence_mode = False
        self.dealer_seat = 0

    def can_call_riichi(self):
        return all([
            self.in_tempai,
            not self.in_riichi,
            self.scores >= 1000,
            self.table.count_of_remaining_tiles > 4
        ])

    @property
    def player_wind(self):
        position = self.dealer_seat
        if position == 0:
            return EAST
        elif position == 1:
            return NORTH
        elif position == 2:
            return WEST
        else:
            return SOUTH

    @property
    def is_dealer(self):
        return self.seat == self.dealer_seat
