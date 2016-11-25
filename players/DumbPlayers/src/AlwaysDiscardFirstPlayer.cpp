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
        return Action(Discard, *it);
    } else {
        Hand copyHand(getHand().getData());
        copyHand.pickTile(tile);
        if (copyHand.testWin()) {
            return Action(Win, tile);
        } else {
            return Action();
        }
    }
}

void AlwaysDiscardFirstPlayer::onOtherPlayerMakeAction(Player *player, Action action) {

}
