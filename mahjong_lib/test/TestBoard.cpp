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

    void onRoundSetup() override {}

    void onRoundStart() override {
        std::cout << "onRoundStart:\n";
    }
    void onBeforePlayerPickTile(Player *player, Tile tile) override {}
    void onAfterPlayerPickTile(Player *player, Tile tile) override {
        std::cout << "onAfterPlayerPickTile:\n";
    }
    void onPlayerDiscardTile(Player *player, Tile tile) override {
        std::cout << "onPlayerDiscardTile:\n";
    }
    void onPlayerPass(Player *player) override {
        std::cout << "onPlayerPass:\n";
    }
    void onRoundFinished(bool drained, Player *winner) override {
        std::cout << "onRoundFinished:\n";
    }
    void onNextRound(bool eastWin) override {

    }

    void onGameOver() override {

    }

    int calculateScore(Hand mHand) override {
        return 0;
    }
};

class TestPlayer : public Player {
 public:
    TestPlayer(std::string playerName) : Player(playerName) {}
    ~TestPlayer() {}

    mahjong::Action onTurn(int playerID, Tile tile) override {
        Tile firstTile = getHand().getTile(0);
        mahjong::Action retAction(mahjong::Discard, firstTile);
        return retAction;
    }

    mahjong::Action onOtherPlayerMakeAction(int playerID, std::string playerName, mahjong::Action action) override {
        return mahjong::Action();
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
    std::string legitOutput = "";
    for (int i = 0; i < 2 * 13; i++) {
        legitOutput += "onAfterPlayerPickTile:\n";
    }
    legitOutput += "onRoundStart:\n";
    for (int i = 0; i < (static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET) - 2 * 13); i++) {
        legitOutput += "onAfterPlayerPickTile:\n"
                "onPlayerDiscardTile:\n"
                "onPlayerPass:\n";
    }
    legitOutput += "onRoundFinished:\n";
    EXPECT_EQ(p1->getHand().getData().size(), 13);
    EXPECT_EQ(p2->getHand().getData().size(), 13);
    delete p1;
    delete p2;
    delete g;
    delete b;
    ASSERT_EQ(output, legitOutput);
}

TEST(TestBoard, General4PlayerBoardTest) {
    TestPlayer *p1 = new TestPlayer("A");
    TestPlayer *p2 = new TestPlayer("B");
    TestPlayer *p3 = new TestPlayer("C");
    TestPlayer *p4 = new TestPlayer("D");
    TestGame *g = new TestGame(p1, p2, p3, p4, 1);
    Board *b = new Board(g, p1, p2, p3, p4, false, 0);

    testing::internal::CaptureStdout();
    // >>> Capture starts.
    b->setup(mahjong::JAPANESE_MAHJONG_TILE_SET, mahjong::East);
    for (int j = 0; j < static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET) - 4 * 13; ++j) {
        b->proceedToNextPlayer();
    }
    b->proceedToNextPlayer();
    // <<< Capture ends.
    std::string output = testing::internal::GetCapturedStdout();
    std::string legitOutput = "";
    for (int i = 0; i < 4 * 13; i++) {
        legitOutput += "onAfterPlayerPickTile:\n";
    }
    legitOutput += "onRoundStart:\n";
    for (int i = 0; i < (static_cast<int>(mahjong::JAPANESE_MAHJONG_TILE_SET) - 4 * 13); i++) {
        legitOutput += "onAfterPlayerPickTile:\n"
                "onPlayerDiscardTile:\n"
                "onPlayerPass:\n"
                "onPlayerPass:\n"
                "onPlayerPass:\n";
    }
    legitOutput += "onRoundFinished:\n";
    EXPECT_EQ(p1->getHand().getData().size(), 13);
    EXPECT_EQ(p2->getHand().getData().size(), 13);
    EXPECT_EQ(p3->getHand().getData().size(), 13);
    EXPECT_EQ(p4->getHand().getData().size(), 13);
    delete p1;
    delete p2;
    delete p3;
    delete p4;
    delete g;
    delete b;
    ASSERT_EQ(output, legitOutput);
}
