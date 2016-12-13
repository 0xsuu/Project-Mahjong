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

#ifndef MAHJONG_LIB_HAND_CATEGORIES_H
#define MAHJONG_LIB_HAND_CATEGORIES_H

namespace mahjong {
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
enum YakuType {
    TsumoHou, // Self-pick.
    Pinfu, // No-points hand.
};

class Yaku {
 public:
    Yaku(const YakuType type, const int point, const std::string name) :
            mType(type), mPoint(point), mName(name) {}

    YakuType getType() const { return mType; }
    int getPoint() const { return mPoint; }
    std::string getName() const { return mName; }

 private:
    YakuType mType;
    int mPoint;
    std::string mName;
};

const Yaku YAKU_TSUMOHOU(TsumoHou, 1, "門前清自摸和(1飜)");
const Yaku YAKU_PINFU(Pinfu, 1, "平和(1飜)");
}
#endif // MAHJONG_LIB_HAND_CATEGORIES_H
