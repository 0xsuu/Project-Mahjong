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

#include <assert.h>

#ifndef WIN32
#include <termio.h>
#include <zconf.h>

int getch() {
    char buf = 0;
    struct termios old = {0};
    if (tcgetattr(0, &old) < 0) {
        perror("tcsetattr()");
    }
    old.c_lflag &= ~ICANON;
    old.c_lflag &= ~ECHO;
    old.c_cc[VMIN] = 1;
    old.c_cc[VTIME] = 0;
    if (tcsetattr(0, TCSANOW, &old) < 0) {
        perror("tcsetattr ICANON");
    }
    if (read(0, &buf, 1) < 0) {
        perror ("read()");
    }
    old.c_lflag |= ICANON;
    old.c_lflag |= ECHO;
    if (tcsetattr(0, TCSADRAIN, &old) < 0) {
        perror ("tcsetattr ~ICANON");
    }
    return (buf);
}
#endif

using std::cin;
using std::cout;
using std::string;
using std::vector;

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

        mSelectionCount = static_cast<int>(getHand().getData().size());

        mSelectIndex = mSelectionCount;
        printPlayerHand(withoutTile, tile);
        printSelectArrow();

        int currentInput = 0;
        while (currentInput != '\n') {
            currentInput = getch();
            switch (currentInput) {
                case 68:
                case 'a':
                    // Left.
                    if (mSelectIndex > 0) {
                        mSelectIndex--;
                        if (mSelectIndex == getHand().getData().size() - 1 ||
                                mSelectIndex == getHand().getData().size() + 1) {
                            mSelectIndex--;
                        }
                    }
                    printPlayer();
                    printPlayerHand(withoutTile, tile);
                    printSelectArrow();
                    break;
                case 67:
                case 'd':
                    // Right.
                    if (mSelectIndex < mSelectionCount) {
                        mSelectIndex++;
                        if (mSelectIndex == getHand().getData().size() - 1 ||
                                mSelectIndex == getHand().getData().size() + 1) {
                            mSelectIndex++;
                        }
                    }
                    printPlayer();
                    printPlayerHand(withoutTile, tile);
                    printSelectArrow();
                    break;
                default:
                    break;
            }
        }

        if (mSelectIndex < getHand().getData().size() - 1) {
            // Find in withoutTile.
            return Action(Discard, withoutTile[mSelectIndex]);
        } else if (mSelectIndex == getHand().getData().size()) {
            // The tile picked.
            std::cout << "Discarding..." << tile.getPrintable() << '\n';
            return Action(Discard, tile);
        } else if (mSelectIndex > getHand().getData().size() + 1) {
            // Actions.
            return Action(mActionSelections[mSelectIndex - getHand().getData().size() - 2], Tile());
        } else {
            throw std::runtime_error("Invalid selection!");
        }
    } else {
        return Action();
    }
}

void UserInputPlayer::onOtherPlayerMakeAction(Player *player, Action action) {

}

void UserInputPlayer::printPlayer() {
    //system("clear");
    cout << MAHJONG_SPECIAL[getSeatPosition()] << ": "
         << getPlayerName() << " ID" << getID() << '\n';
}

void UserInputPlayer::printPlayerHand(TileGroup g, Tile t) {
    string outputLine = g.getPrintable() + "|" + TILES_SEPARATE_PATTERN
                        + t.getPrintable() + TILES_SEPARATE_PATTERN;
    mActionSelections.clear();

    bool canWin = getHand().testWin();

    if (canWin) {
        mActionSelections.push_back(Win);
        mSelectionCount = static_cast<int>(getHand().getData().size()) + 1;
        outputLine = outputLine + "->";
    }

    if (!canWin) {
        mSelectionCount = static_cast<int>(getHand().getData().size());
    }

    if (canWin) {
        mSelectionCount++;
        outputLine = outputLine + TILES_SEPARATE_PATTERN + "Win!";
    }

    cout << outputLine << '\n';
}

void UserInputPlayer::printSelectArrow() {
    assert(mSelectIndex != getHand().getData().size() - 1);
    for (int i = 0; i < mSelectIndex; ++i) {
        cout << TILES_SEPARATE_PATTERN;
    }
    cout << '^' << '\n';
}
