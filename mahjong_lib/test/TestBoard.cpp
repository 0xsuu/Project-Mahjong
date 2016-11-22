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

#include <gtest/gtest.h>

#include <iostream>
#include <vector>

#include <Board.h>
#include <Game.h>
#include <Hand.h>
#include <Player.h>

using std::vector;

using mahjong::Board;
using mahjong::Game;
using mahjong::Hand;
using mahjong::Player;
using mahjong::Tile;

class TestGame : public Game {
 public:
    TestGame(Player *p1, Player *p2, Player *p3, Player *p4, int roundCounts) :
            Game(p1, p2, p3, p4, roundCounts) {}
    ~TestGame() {}

    void startGame() override {

    }

    void onRoundStart() override {
        std::cout << "onRoundStart:\n";
    }
    void onPlayerPass(Player *player) override {
        std::cout << "onPlayerPass:\n";
    }
    void onTileDrawToPlayer(Player *player, Tile tile) override {
        std::cout << "onTileDrawToPlayer:\n";
    }
    void onPlayerDiscardTile(Player *player, Tile tile) override {
        std::cout << "onPlayerDiscardTile:\n";
    }
    void onRoundFinished(bool drained, Player *winner) override {
        std::cout << "onRoundFinished:\n";
    }

    int calculateScore(Hand mHand) override {
        return 0;
    }
};

class TestPlayer : public Player {
 public:
    TestPlayer(std::string playerName) : Player(playerName) {}
    ~TestPlayer() {}

    mahjong::Action onTurn(bool isMyTurn, Tile tile) override {
        if (!isMyTurn) {
            return mahjong::Action();
        } else {
            Tile firstTile = getHand().getTile(0);
            mahjong::Action retAction(mahjong::Discard, firstTile);
            return retAction;
        }
    }

    void onOtherPlayerMakeAction(Player *player, mahjong::Action action) override {

    }
};

TEST(TestBoard, General2PlayerBoardTest) {
    TestPlayer *p1 = new TestPlayer("A");
    TestPlayer *p2 = new TestPlayer("B");
    TestGame *g = new TestGame(p1, p2, nullptr, nullptr, 1);
    Board *b = new Board(g, p1, p2, nullptr, nullptr, false, 0);

    testing::internal::CaptureStdout();
    // >>> Capture starts.
    b->setup(mahjong::JAPANESE_MAHJONG_TILE_SET, mahjong::East);
    for (int j = 0; j < static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET) - 2 * 13; ++j) {
        b->proceedToNextPlayer();
    }
    b->proceedToNextPlayer();
    // <<< Capture ends.
    std::string output = testing::internal::GetCapturedStdout();
    std::string legitOutput = "onRoundStart:\n";
    for (int i = 0; i < 2 * 13; i++) {
        legitOutput += "onTileDrawToPlayer:\n";
    }
    for (int i = 0; i < (static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET) - 2 * 13) / 2; i++) {
        legitOutput += "onTileDrawToPlayer:\n"
                "onPlayerDiscardTile:\n"
                "onTileDrawToPlayer:\n"
                "onPlayerPass:\n"
                "onTileDrawToPlayer:\n"
                "onPlayerPass:\n"
                "onTileDrawToPlayer:\n"
                "onPlayerDiscardTile:\n";
    }
    legitOutput += "onRoundFinished:\n";
    delete p1;
    delete p2;
    delete g;
    delete b;
    ASSERT_EQ(output, legitOutput);
}
