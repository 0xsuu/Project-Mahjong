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

#include "UserInputPlayer.h"

#include <iomanip>
#include <iostream>

#include <PrintFormat.h>

using std::cin;
using std::cout;
using std::string;

using mahjong::Action;
using mahjong::Player;
using mahjong::Tile;
using mahjong::TileGroup;
using mahjong::UserInputPlayer;

Action UserInputPlayer::onTurn(bool isMyTurn, Tile tile) {
    if (isMyTurn) {
        printPlayer();
        TileGroup withoutTile(getHand().getData());
        withoutTile.removeTile(tile);
        string selectOutputLine = withoutTile.getPrintable() + "| " + tile.getPrintable();
        cout << selectOutputLine << '\n';

        int act;
        cin >> act;

        if (act == 100) {
            return Action(Win, Tile());
        }

        system("clear");

        return Action(Discard, act == withoutTile.getData().size() ? tile : withoutTile[act]);
    } else {
        return Action();
    }
}

void UserInputPlayer::onOtherPlayerMakeAction(Player *player, Action action) {

}

void UserInputPlayer::printPlayer() {
    cout << MAHJONG_SPECIAL[getSeatPosition()] << ": "
         << getPlayerName() << " ID" << getID() << '\n';
}
