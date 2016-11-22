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

#include "SimpleGame.h"

class TestPlayer : public mahjong::Player {
 public:
    TestPlayer(std::string playerName) : mahjong::Player(playerName) {}
    ~TestPlayer() {}

    mahjong::Action onTurn(bool isMyTurn, mahjong::Tile tile) override {
        if (!isMyTurn) {
            return mahjong::Action();
        } else {
            mahjong::Tile firstTile = getHand().getTile(0);
            mahjong::Action retAction(mahjong::Discard, firstTile);
            return retAction;
        }
    }

    void onOtherPlayerMakeAction(mahjong::Player *player, mahjong::Action action) override {

    }
};

using mahjong::SimpleGame;

int main() {
    TestPlayer *p1 = new TestPlayer("A");
    TestPlayer *p2 = new TestPlayer("B");
    SimpleGame *game = new SimpleGame(p1, p2, nullptr, nullptr, 1);

    game->startGame();

    return 0;
}
