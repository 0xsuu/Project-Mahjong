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

#include <termios.h>
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
#endif // WIN32

#define MIN_SELECTION_COUNT_FOR_NOT_MY_TURN 1

using std::cin;
using std::cout;
using std::string;
using std::vector;

using mahjong::Action;
using mahjong::Player;
using mahjong::Tile;
using mahjong::TileGroup;
using mahjong::UserInputPlayer;

Action UserInputPlayer::onTurn(int playerID, Tile tile) {
    mIsMyTurn = getID() == playerID;
    mCurrentPlayerID = playerID;
    if (mIsMyTurn) {
        TileGroup withoutTile(getHand().getData());
        withoutTile.removeTile(tile);

        if (getActionSelections(Tile())) {
            constructBoardString(withoutTile, tile);
            addActionSelectionDialog();
            ActionState selectedActionState = mActionStateSelections[mSelectIndex - MIN_SELECTION_COUNT_FOR_NOT_MY_TURN];
            if (selectedActionState == Cancel) {
                constructBoardString(withoutTile, tile);
                addDiscardTileDialog(withoutTile);
                return Action(Discard, getDiscardTileDialogSelection(withoutTile, tile));
            } else {
                return Action(selectedActionState, (selectedActionState == Win) ? Tile() : tile);
            }
        } else {
            constructBoardString(withoutTile, tile);
            addDiscardTileDialog(withoutTile);
            return Action(Discard, getDiscardTileDialogSelection(withoutTile, tile));
        }
    }
}

Action UserInputPlayer::onOtherPlayerMakeAction(int playerID, std::string playerName, Action action) {
    mIsMyTurn = getID() == playerID;
    mCurrentPlayerID = playerID;

    constructBoardString(getHand(), Tile());

    if (getActionSelections(action.getTile())) {
        mCurrentBoard = mCurrentBoard + "\n\nPlayer ID" + std::to_string(playerID) + " discarded " + action.getTile().getPrintable() + ":";
        addActionSelectionDialog();
        ActionState selectedActionState = mActionStateSelections[mSelectIndex -
                                                                 MIN_SELECTION_COUNT_FOR_NOT_MY_TURN];
        return Action(selectedActionState, action.getTile());
    } else {
        return Action();
    }
}

void UserInputPlayer::addDiscardTileDialog(TileGroup withoutTile) {
    auto withoutTileData = withoutTile.getData();
    auto it = withoutTileData.begin();
    while ((*it).getFlag() != Handed) {
        it++;
    }
    int firstHandedIndex = static_cast<int>(std::distance(withoutTileData.begin(), it));
    takeSelectionLineInputs(firstHandedIndex, static_cast<int>(withoutTile.getData().size()) + 1,
                            static_cast<int>(withoutTile.getData().size()) + 1,
                            {static_cast<int>(withoutTile.getData().size())});
}

Tile UserInputPlayer::getDiscardTileDialogSelection(TileGroup withoutTile, Tile tile) {
    if (mSelectIndex == getHand().getData().size()) {
        // The tile picked.
        return tile;
    } else if (mSelectIndex < getHand().getData().size()) {
        return withoutTile[mSelectIndex];
    } else {
        throw std::runtime_error("Invalid selection!");
    }
}

void UserInputPlayer::printBoard() {
    system("clear");

    cout << mCurrentBoard << '\n';
}

void UserInputPlayer::constructBoardString(TileGroup g, Tile t) {
    mCurrentBoard = "";

    // Add all players' discarded tiles.
    auto playerIDAndDiscardedTiles = getPlayerIDAndDiscardedTiles();
    for (auto it = playerIDAndDiscardedTiles.begin(); it != playerIDAndDiscardedTiles.end(); it++) {
        mCurrentBoard += (*it).second + "\n\n";
    }

    // Add Player information.
    mCurrentBoard += getPrintable() + "\n";

    // Add Player hand information.
    mCurrentBoard += g.getPrintable() + "|" + (!t.isNull() ?
                                               (TILES_SEPARATE_PATTERN +
                                                t.getPrintable()) : "");
}

void UserInputPlayer::printSelectArrow() {
    for (int i = 0; i < mSelectIndex; ++i) {
        cout << TILES_SEPARATE_PATTERN;
    }
    cout << "☝" << '\n';
}

bool UserInputPlayer::getActionSelections(Tile addedTile) {
    mActionStateSelections.clear();
    bool canWin;
    if (addedTile.isNull()) {
        canWin = getHand().testWin();
    } else {
        Hand copyHand(getHand().getData());
        copyHand.pickTile(addedTile);
        canWin = copyHand.testWin();
    }

    if (canWin) {
        mActionStateSelections.push_back(Win);
    }

    if (canWin /*||*/) {
        if (!mIsMyTurn) {
            mActionStateSelections.push_back(Pass);
        } else {
            mActionStateSelections.push_back(Cancel);
        }
        return true;
    } else {
        return false;
    }
}

void UserInputPlayer::addActionSelectionDialog() {
    string outputLine = "";
    outputLine = outputLine + "->" + TILES_SEPARATE_PATTERN;
    std::for_each(mActionStateSelections.begin(), mActionStateSelections.end(), [&](ActionState as) {
        outputLine += MAHJONG_ACTION_STATES[as] + TILES_SEPARATE_PATTERN;
    });
    mCurrentBoard += "\n" + outputLine + "\n";

    takeSelectionLineInputs(1, static_cast<int>(mActionStateSelections.size()), 1, {});
}

void UserInputPlayer::takeSelectionLineInputs(int minSelection, int maxSelection, int initialIndex,
                                              std::vector<int> nonSelectionIndexes) {
    mSelectionCount = maxSelection;
    mSelectIndex = initialIndex;

    printBoard();
    printSelectArrow();

    int currentInput = 0;
    while (currentInput != '\n') {
        currentInput = getch();
        switch (currentInput) {
            case 68:
            case 'a':
                // Left.
                if (mSelectIndex > minSelection) {
                    mSelectIndex--;
                    if (!nonSelectionIndexes.empty() &&
                            std::find(nonSelectionIndexes.begin(), nonSelectionIndexes.end(), mSelectIndex)
                            != nonSelectionIndexes.end()) {
                        mSelectIndex--;
                        if (mSelectIndex < minSelection) {
                            mSelectIndex = mSelectionCount;
                        }
                    }
                } else if (mSelectIndex == minSelection) {
                    mSelectIndex = mSelectionCount;
                }
                printBoard();
                printSelectArrow();
                break;
            case 67:
            case 'd':
                // Right.
                if (mSelectIndex < mSelectionCount) {
                    mSelectIndex++;
                    if (!nonSelectionIndexes.empty() &&
                            std::find(nonSelectionIndexes.begin(), nonSelectionIndexes.end(), mSelectIndex)
                            != nonSelectionIndexes.end()) {
                        mSelectIndex++;
                        if (mSelectIndex > mSelectionCount) {
                            mSelectIndex = minSelection;
                        }
                    }
                } else if (mSelectIndex == mSelectionCount) {
                    mSelectIndex = minSelection;
                }
                printBoard();
                printSelectArrow();
                break;
            default:
                break;
        }
    }
}
