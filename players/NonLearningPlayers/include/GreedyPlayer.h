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

#ifndef MAHJONG_PLAYER_GREEDY_PLAYER_H
#define MAHJONG_PLAYER_GREEDY_PLAYER_H

#include <Player.h>

namespace mahjong {
class GreedyPlayer : public Player {
 public:
    GreedyPlayer(std::string playerName) : Player(playerName) {}

    Action onTurn(int playerID, Tile tile) override;
    Action onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) override;

    const Tile selectBestTile(Hand hand);

 private:
    int getHeuristic(Hand hand);
};
}
#endif // MAHJONG_PLAYER_GREEDY_PLAYER_H
