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

#ifndef MAHJONG_LIB_TENHOU_ENCODER_H
#define MAHJONG_LIB_TENHOU_ENCODER_H

#include <vector>

#include <Constants.h>

#include "document.h"
#include "writer.h"
#include "stringbuffer.h"

namespace mahjong {
/**
 * Saving using JSON.
 *
 * Example:
 * {"title":["第二期　天鳳名人戦", "第１節　Ａ卓　１戦目"],
 * "name":["Ⓢ福地誠","Ⓟ多井隆晴","Cさん","Ⓟ石橋伸洋"],
 * "rule":{"disp":"般南喰赤","aka":1},
 * "log":[[[0,0,0],
 * [30000,30000,30000,30000],[24],[],
 * [12,17,21,22,25,26,27,32,33,34,37,37,43],
 * [39,32,46,35,"32p3232",33,"37p3737",31],
 * [43,39,12,46,21,22,17,60],
 * [16,16,19,22,22,23,26,27,29,39,42,45,47],
 * [13,28,38,21,26,23,18,12],
 * [19,39,45,38,42,47,13,60],
 * [11,11,14,15,16,17,19,28,37,41,43,44,46],
 * [41,14,"1111p11",38,32,35,37,33,14],
 * [28,37,43,60,60,60,60,44,33],
 * [11,51,17,18,24,52,32,33,36,36,43,44,45],
 * [31,21,26,19,44,18],
 * [43,11,45,44,60,60],
 * ["和了",[2900,0,-2900,0],[0,2,0,"30符2飜2900点","断幺九(1飜)","ドラ(1飜)"]]]]}
 *
 * Explanation:
 * {"title": [Array of Titles],
 *  "name": [Array of Players' names],
 *  "rule": {"disp":"表記名", "aka":Number of Aka dora tile}, // Alternative: aka51:2 aka52:1 aka53:1.
 *  "log":[[
 *      [Round(e.g. 東1局), Sub-round(e.g. 一本场), 供託],
 *      [Players' points], [Dora tiles], [Hidden dora tiles],
 *      [Player1's initial hand],
 *      [Players's picked tiles], // String means stealing tiles from others.
 *      [Player1's discarded tiles],
 *      [Player2's initial hand],
 *      [Player2's picked tiles],
 *      [Player2's discarded tiles],
 *      [Player3's initial hand],
 *      [Player3's picked tiles],
 *      [Player3's discarded tiles],
 *      [Player4's initial hand],
 *      [Player4's picked tiles],
 *      [Player4's discarded tiles],
 *      ["Result of the game", [players' points +-],
 *          [,,,"Winning points", "Winning hand types details"]]
 *  ]]}
 *
 * Tiles encoding:
 * m: Character
 * p: Dot
 * s: Bamboo
 * z: Special
 *
 * 11 - 19: 1m - 9m
 * 21 - 29: 1p - 9p
 * 31 - 39: 1s - 9s
 * 41 - 47: 1z - 7z
 * 60: Discard picked tile
 */

/**
 * This class is capable for generate Tenhou specified
 */
class TenhouEncoder {
 public:
    TenhouEncoder() {
        mWriter.Reset(mStringBuffer);
        mWriter.StartObject();
    }

    void setTitles(std::vector<std::string> titles);
    void setPlayerNames(std::vector<std::string> names);
    void setRules(std::string ruleName, int aka);
    void setRules(std::string ruleName, int aka51, int aka52, int aka53);
    /**
     * Call after game ends.
     *
     * @param round
     * @param subRound
     * @param number
     * @param playerPoints
     * @param doraTiles
     * @param hiddenDoraTiles
     * @param initialHands
     * @param pickedTileGroups
     * @param discardedTileGroups
     * @param result
     * @param pointVariants
     * @param opponentStates
     * @param winningPointsString
     * @param winningHandNames
     */
    void setLogs(int round, int subRound, int number,
                 std::vector<int> playerPoints,
                 std::vector<int> doraTiles, std::vector<int> hiddenDoraTiles,
                 std::vector<mahjong::TileGroup> initialHands,
                 std::vector<mahjong::TileGroup> pickedTileGroups,
                 std::vector<mahjong::TileGroup> discardedTileGroups,
                 std::string result,
                 std::vector<int> pointVariants,
                 std::vector<int> opponentStates,
                 std::string winningPointsString,
                 std::vector<std::string> winningHandNames);

    std::string getString();

 private:
    rapidjson::StringBuffer mStringBuffer;
    rapidjson::Writer<rapidjson::StringBuffer> mWriter;

    rapidjson::Document mJSONObject;

    void writeArray(std::vector<std::string> arr);
    void writeArray(std::vector<int> arr);
    void writeArray(mahjong::TileGroup arr);
    int toTenhouTile(Tile t);
};
} // namespace mahjong.
#endif //MAHJONG_LIB_TENHOU_ENCODER_H
