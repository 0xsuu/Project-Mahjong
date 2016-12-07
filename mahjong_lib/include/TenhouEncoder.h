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
 * "name": [Array of Players' names],
 * "rule": {"disp":"表記名", "aka":Number of Aka dora tile}, // Alternative: aka51:2 aka52:1 aka53:1.
 * "log":[[[Round(e.g. 東1局), Sub-round(e.g. 一本场), 供託],
 * [Players' points], [Dora tiles], [Hidden dora tiles],
 * [Player1's initial hand],
 * [Players's picked tiles], // String means stealing tiles from others.
 * [Player1's discarded tiles],
 * [Player2's initial hand],
 * [Player2's picked tiles],
 * [Player2's discarded tiles],
 * [Player3's initial hand],
 * [Player3's picked tiles],
 * [Player3's discarded tiles],
 * [Player4's initial hand],
 * [Player4's picked tiles],
 * [Player4's discarded tiles],
 * ["Result", [players' points +-], [,,,"Winning points", "Winning hand types details"]]]]]}
 */

/**
 * Winning types and fan.
 *
 * 門前清自摸和(1飜)
 * 立直(1飜)
 * 一発(1飜) 一発(1飜1枚) 一発(1枚)
 * 槍槓(1飜)
 * 嶺上開花(1飜)
 * 海底摸月(1飜)
 * 河底撈魚(1飜)
 * 平和(1飜)
 * 断幺九(1飜)
 * 一盃口(1飜)
 * 自風 東(1飜) 自風 南(1飜) 自風 西(1飜) 自風 北(1飜)
 * 場風 東(1飜) 場風 南(1飜) 場風 西(1飜) 場風 北(1飜)
 * 役牌 白(1飜) 役牌 發(1飜) 役牌 中(1飜)
 * 両立直(2飜)
 * 七対子(1飜) 七対子(2飜)
 * 混全帯幺九(1飜) 混全帯幺九(2飜)
 * 一気通貫(1飜) 一気通貫(2飜)
 * 三色同順(1飜) 三色同順(2飜)
 * 三色同刻(2飜)
 * 三槓子(2飜)
 * 対々和(2飜)
 * 三暗刻(2飜)
 * 小三元(2飜)
 * 混老頭(2飜)
 * 二盃口(3飜)
 * 純全帯幺九(2飜) 純全帯幺九(3飜)
 * 混一色(2飜) 混一色(3飜)
 * 清一色(5飜) 清一色(6飜)
 * 天和(役満) 天和(役満5枚) 天和(役満10枚)
 * 地和(役満) 地和(役満5枚) 地和(役満10枚)
 * 大三元(役満) 大三元(役満5枚) 大三元(役満10枚)
 * 四暗刻(役満) 四暗刻(役満5枚) 四暗刻(役満10枚)
 * 四暗刻単騎(役満) 四暗刻単騎(役満5枚) 四暗刻単騎(役満10枚)
 * 字一色(役満) 字一色(役満5枚) 字一色(役満10枚)
 * 緑一色(役満) 緑一色(役満5枚) 緑一色(役満10枚)
 * 清老頭(役満) 清老頭(役満5枚) 清老頭(役満10枚)
 * 九蓮宝燈(役満) 九蓮宝燈(役満5枚) 九蓮宝燈(役満10枚)
 * 純正九蓮宝燈(役満) 純正九蓮宝燈(役満5枚) 純正九蓮宝燈(役満10枚)
 * 国士無双(役満) 国士無双(役満5枚) 国士無双(役満10枚)
 * 国士無双１３面(役満) 国士無双１３面(役満5枚) 国士無双１３面(役満10枚)
 * 大四喜(役満) 大四喜(役満5枚) 大四喜(役満10枚)
 * 小四喜(役満) 小四喜(役満5枚) 小四喜(役満10枚)
 * 四槓子(役満) 四槓子(役満5枚) 四槓子(役満10枚)
 */

class TenhouEncoder {
 public:
    TenhouEncoder() {}

    std::string getString();

 private:
    rapidjson::Document mJSONObject;
};
} // namespace mahjong.
#endif //MAHJONG_LIB_TENHOU_ENCODER_H
