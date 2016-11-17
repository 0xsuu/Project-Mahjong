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

#include <numeric>
#include <vector>

#include <gtest/gtest.h>

#include <TileStack.h>

using std::vector;

using mahjong::TileStack;

TEST(TestTileStack, TileStackDice) {
    TileStack tileStack(JAPANESE_MAHJONG_TILES_COUNT, false, 0);
    vector<int> diceCount = {0, 0, 0, 0, 0, 0};
    for (int i = 0; i < 100000; ++i) {
        diceCount[tileStack.throwDice() - 1] ++;
    }

    double sum = std::accumulate(diceCount.begin(), diceCount.end(), 0);

    EXPECT_NEAR(1.0 / 6.0, diceCount[0] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[1] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[2] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[3] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[4] / sum, 0.01);
    EXPECT_NEAR(1.0 / 6.0, diceCount[5] / sum, 0.01);
}

TEST(TestTileStack, TileStackRandomDrawTile) {

}
