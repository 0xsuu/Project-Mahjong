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

Action AlwaysDiscardFirstPlayer::onTurn(bool isMyTurn, Tile tile) {
    if (isMyTurn) {
        if (getHand().testWin()) {
            return Action(Win, Tile());
        }
        auto it = getHand().getData().begin();
        while ((*it).getFlag() != mahjong::Handed) {
            it++;
        }
        assert(it != getHand().getData().end() && "This is impossible! You don't have one tile in hand?");
        // std::cout << "My hand: " << getHand().getPrintable() << '\n';
        return Action(Discard, *it);
    } else {
        return Action();
    }
}

void AlwaysDiscardFirstPlayer::onOtherPlayerMakeAction(Player *player, Action action) {

}
