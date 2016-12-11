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
#include <UserInputPlayer.h>
#include <AlwaysDiscardFirstPlayer.h>
#include <RandomPlayer.h>
#include <AlwaysLosePlayer.h>
#include <GreedyPlayer.h>

using mahjong::SimpleGame;
using mahjong::UserInputPlayer;
using mahjong::AlwaysDiscardFirstPlayer;
using mahjong::RandomPlayer;
using mahjong::AlwaysLosePlayer;
using mahjong::GreedyPlayer;

int main() {
    GreedyPlayer *p1 = new GreedyPlayer("BOT Greedy");
    AlwaysDiscardFirstPlayer *p2 = new AlwaysDiscardFirstPlayer("BOT ADFT");
    AlwaysDiscardFirstPlayer *p3 = new AlwaysDiscardFirstPlayer("BOT ADFT 3");
    AlwaysDiscardFirstPlayer *p4 = new AlwaysDiscardFirstPlayer("BOT ADFT 4");
//    mahjong::Player *p3 = nullptr;
//    mahjong::Player *p4 = nullptr;
    SimpleGame *game = new SimpleGame(p1, p2, p3, p4, 1000);

    game->startGame();

    return 0;
}
