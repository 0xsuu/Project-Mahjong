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

#include "GreedyPlayer.h"

using mahjong::Action;
using mahjong::GreedyPlayer;

Action GreedyPlayer::onTurn(int playerID, Tile tile) {
    if (playerID == getID()) {
        if (getHand().testWin()) {
            return Action(Win, Tile());
        }
        auto handData = getHand().getData();
        auto it = handData.begin();
        while ((*it).getFlag() != mahjong::Handed) {
            it++;
        }

        auto maxIt = it;
        auto maxHeu = -1;
        for (; it < handData.end(); it ++) {
            auto handDataWithoutIt(handData);
            handDataWithoutIt.erase(handDataWithoutIt.begin() + std::distance(handData.begin(), it));
            int heu = getHeuristic(handDataWithoutIt);
            if (heu > maxHeu) {
                maxHeu = heu;
                maxIt = it;
            }
        }

        return Action(Discard, *maxIt);
    } else {
        return Action();
    }
}

Action GreedyPlayer::onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) {
    Hand copyHand(getHand().getData());
    copyHand.pickTile(action.getTile());
    if (copyHand.testWin()) {
        return Action(Win, action.getTile());
    } else {
        return Action();
    }
}

int GreedyPlayer::getHeuristic(Hand hand) {
    int straight = 0;
    int kang = 0;
    int pong = 0;
    int straightOfTwo = 0;
    int pongOfTwo = 0;

    auto handData = hand.getData();
    for (auto it = handData.begin(); it < handData.end() - 2; it++) {
        auto itNext = std::find(it, handData.end(), *it + 1);
        if (itNext < handData.end() - 1) {
            auto itNextNext = std::find(itNext, handData.end(), *itNext + 1);
            if (itNextNext < handData.end()) {
                straight++;
            }
        }
    }
    for (auto it = handData.begin(); it < handData.end() - 3; it++) {
        if (*it == *(it + 1) && *(it + 1) == *(it + 2) && *(it + 2) == *(it + 3)) {
            if (((*it).getFlag() == Concealed | (*it).getFlag() == Melded) &&
                   ((*it + 1).getFlag() == Concealed | (*it + 1).getFlag() == Melded) &&
                   ((*it + 2).getFlag() == Concealed | (*it + 2).getFlag() == Melded) &&
                   ((*it + 3).getFlag() == Concealed | (*it + 3).getFlag() == Melded)) {
                kang++;
            }
        }
    }
    for (auto it = handData.begin(); it < handData.end() - 2; it++) {
        if (*it == *(it + 1) && *(it + 1) == *(it + 2)) {
            pong++;
        }
    }
    for (auto it = handData.begin(); it < handData.end() - 1; it++) {
        if (*it == *(it + 1)) {
            pongOfTwo++;
        }
    }
    for (auto it = handData.begin(); it < handData.end() - 2; it++) {
        if ((*it).getType() == Special) {
            break;
        }
        auto itNext = std::find(it, handData.end(), *it + 1);
        if (itNext < handData.end() - 1) {
            straightOfTwo++;
        }
    }
    return straight * 100 + kang * 110 + pong * 100 + pongOfTwo * 50 + straightOfTwo * 50;
}
