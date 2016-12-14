//
//  Copyright © 2016 Project Mahjong. All rights reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.
//

#include <assert.h>
#include <iostream>
#include "AlwaysDiscardFirstPlayer.h"

using mahjong::Action;
using mahjong::Player;
using mahjong::Tile;
using mahjong::TileGroup;
using mahjong::AlwaysDiscardFirstPlayer;

Action AlwaysDiscardFirstPlayer::onTurn(int playerID, Tile tile) {
#ifdef SIMPLE_MAHJONG
    if (playerID == getID()) {
        if (getHand().testWin()) {
            return Action(Win, Tile());
        }
        auto handData = getHand().getData();
        auto it = handData.begin();
        while ((*it).getFlag() != mahjong::Handed) {
            it++;
        }
        assert(it != handData.end() && "This is impossible! You don't have one tile in hand?");
        return Action(Discard, *it);
    } else {
        return Action();
    }
#else
    throw std::runtime_error("No games are defined for this player.");
#endif
}

Action AlwaysDiscardFirstPlayer::onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) {
    Hand copyHand(getHand().getData());
    copyHand.pickTile(action.getTile());
    if (copyHand.testWin()) {
        return Action(Win, action.getTile());
    } else {
        return Action();
    }
}
