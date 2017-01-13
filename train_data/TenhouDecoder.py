#!/usr/bin/env python3

'''
 The MIT License (MIT)

 Copyright (c) 2014 Mark Haines

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

import xml.etree.ElementTree as etree
import urllib.parse
from Data import Data

class Tile(Data, int):
    UNICODE_TILES = """
        🀐 🀑 🀒 🀓 🀔 🀕 🀖 🀗 🀘
        🀙 🀚 🀛 🀜 🀝 🀞 🀟 🀠 🀡
        🀇 🀈 🀉 🀊 🀋 🀌 🀍 🀎 🀏 
        🀀 🀁 🀂 🀃
        🀆 🀅 🀄
    """.split()

    TILES = """
        1m 2m 3m 4m 5m 6m 7m 8m 9m
        1p 2p 3p 4p 5p 6p 7p 8p 9p
        1s 2s 3s 4s 5s 6s 7s 8s 9s
        ew sw ww nw
        wd gd rd
    """.split()

    def asdata(self, convert = None):
        return self.TILES[self // 4]
        
class Player(Data):
    pass    

class Round(Data):
    pass

class Meld(Data):
    @classmethod
    def decode(Meld, data):
        data = int(data)
        meld = Meld()
        meld.fromPlayer = data & 0x3
        if data & 0x4:
            meld.decodeChi(data)
        elif data & 0x18:
            meld.decodePon(data)
        elif data & 0x20:
            meld.decodeNuki(data)
        else:
            meld.decodeKan(data)
        return meld

    def decodeChi(self, data):
        self.type = "chi"
        t0, t1, t2 = (data >> 3) & 0x3, (data >> 5) & 0x3, (data >> 7) & 0x3
        baseAndCalled = data >> 10
        self.called = baseAndCalled % 3
        base = baseAndCalled // 3
        base = (base // 7) * 9 + base % 7
        self.tiles = Tile(t0 + 4 * (base + 0)), Tile(t1 + 4 * (base + 1)), Tile(t2 + 4 * (base + 2))
    
    def decodePon(self, data):
        t4 = (data >> 5) & 0x3
        t0, t1, t2 = ((1,2,3),(0,2,3),(0,1,3),(0,1,2))[t4]
        baseAndCalled = data >> 9
        self.called = baseAndCalled % 3
        base = baseAndCalled // 3
        if data & 0x8:
            self.type = "pon"
            self.tiles = Tile(t0 + 4 * base), Tile(t1 + 4 * base), Tile(t2 + 4 * base)
        else:
            self.type = "chakan"
            self.tiles = Tile(t0 + 4 * base), Tile(t1 + 4 * base), Tile(t2 + 4 * base), Tile(t4 + 4 * base)
    
    def decodeKan(self, data):
        baseAndCalled = data >> 8
        if self.fromPlayer:
            self.called = baseAndCalled % 4
        else:
            del self.fromPlayer
        base = baseAndCalled // 4
        self.type = "kan"
        self.tiles = Tile(4 * base), Tile(1 + 4 * base), Tile(2 + 4 * base), Tile(3 + 4 * base)

    def decodeNuki(self, data):
        del self.fromPlayer
        self.type = "nuki"
        self.tiles = Tile(data >> 8)

class Event(Data):
    def __init__(self, events):
        events.append(self)
        self.type = type(self).__name__

class Dora(Event):
    pass

class Draw(Event):
    pass

class Discard(Event):
    pass

class Call(Event):
    pass

class Riichi(Event):
    pass

class Agari(Data):
    pass

class Game(Data):
    RANKS = "新人,9級,8級,7級,6級,5級,4級,3級,2級,1級,初段,二段,三段,四段,五段,六段,七段,八段,九段,十段,天鳳位".split(",")
    NAMES = "n0,n1,n2,n3".split(",")
    HANDS = "hai0,hai1,hai2,hai3".split(",")
    ROUND_NAMES = "東1,東2,東3,東4,南1,南2,南3,南4,西1,西2,西3,西4,北1,北2,北3,北4".split(",")
    YAKU = (
            # 一飜
            'mentsumo',        # 門前清自摸和
            'riichi',          # 立直
            'ippatsu',         # 一発
            'chankan',         # 槍槓
            'rinshan kaihou',  # 嶺上開花
            'haitei raoyue',   # 海底摸月
            'houtei raoyui',   # 河底撈魚
            'pinfu',           # 平和
            'tanyao',          # 断幺九
            'iipeiko',         # 一盃口
            # seat winds
            'ton',             # 自風 東
            'nan',             # 自風 南
            'xia',             # 自風 西
            'pei',             # 自風 北
            # round winds
            'ton',             # 場風 東
            'nan',             # 場風 南
            'xia',             # 場風 西
            'pei',             # 場風 北
            'haku',            # 役牌 白
            'hatsu',           # 役牌 發
            'chun',            # 役牌 中
            # 二飜
            'daburu riichi',   # 両立直
            'chiitoitsu',      # 七対子
            'chanta',          # 混全帯幺九
            'ittsu',           # 一気通貫
            'sanshoku doujun', # 三色同順
            'sanshoku doukou', # 三色同刻
            'sankantsu',       # 三槓子
            'toitoi',          # 対々和
            'sanankou',        # 三暗刻
            'shousangen',      # 小三元
            'honroutou',       # 混老頭
            # 三飜
            'ryanpeikou',      # 二盃口
            'junchan',         # 純全帯幺九
            'honitsu',         # 混一色
            # 六飜
            'chinitsu',        # 清一色
            # 満貫
            'renhou',          # 人和
            # 役満
            'tenhou',                # 天和
            'chihou',                # 地和
            'daisangen',             # 大三元
            'suuankou',              # 四暗刻
            'suuankou tanki',        # 四暗刻単騎
            'tsuuiisou',             # 字一色
            'ryuuiisou',             # 緑一色
            'chinroutou',            # 清老頭
            'chuuren pouto',         # 九蓮宝燈
            'chuuren pouto 9-wait',  # 純正九蓮宝燈
            'kokushi musou',         # 国士無双
            'kokushi musou 13-wait', # 国士無双１３面
            'daisuushi',             # 大四喜
            'shousuushi',            # 小四喜
            'suukantsu',             # 四槓子
            # 懸賞役
            'dora',    # ドラ
            'uradora', # 裏ドラ
            'akadora', # 赤ドラ
            )
    LIMITS=",mangan,haneman,baiman,sanbaiman,yakuman".split(",")

    TAGS = {}
    
    def tagGO(self, tag, data):
        self.gameType = data["type"]
        # The <GO lobby=""/> attribute was introduced at some point between
        # 2010 and 2012:
        self.lobby = data.get("lobby")

    def tagUN(self, tag, data):
        if "dan" in data:
            for name in self.NAMES:
                # An empty name, along with sex C, rank 0 and rate 1500 are
                # used as placeholders in the fourth player fields in
                # three-player games
                if data[name]:
                    player = Player()
                    player.name = urllib.parse.unquote(data[name])
                    self.players.append(player)
            ranks = self.decodeList(data["dan"])
            sexes = self.decodeList(data["sx"], dtype = str)
            rates = self.decodeList(data["rate"], dtype = float)
            for (player, rank, sex, rate) in zip(self.players, ranks, sexes, rates):
                player.rank = self.RANKS[rank]
                player.sex = sex
                player.rate = rate
                player.connected = True
        else:
            for (player, name) in zip(self.players, self.NAMES):
                if name in data:
                    player.connected = True
    
    def tagBYE(self, tag, data):
        self.players[int(data["who"])].connected = False

    def tagINIT(self, tag, data):
        self.round = Round()
        self.rounds.append(self.round)
        name, combo, riichi, d0, d1, dora = self.decodeList(data["seed"])
        self.round.round = self.ROUND_NAMES[name], combo, riichi
        self.round.hands = tuple(self.decodeList(data[hand], Tile) for hand in self.HANDS if hand in data and data[hand])
        self.round.dealer = int(data["oya"])
        self.round.events = []
        self.round.agari = []
        self.round.ryuukyoku = False
        self.round.ryuukyoku_tenpai = None
        Dora(self.round.events).tile = Tile(dora)

    def tagN(self, tag, data):
        call = Call(self.round.events)
        call.meld = Meld.decode(data["m"])
        call.player = int(data["who"])

    def tagTAIKYOKU(self, tag, data):
        pass

    def tagDORA(self, tag, data):
        Dora(self.round.events).tile = int(data["hai"])

    def tagRYUUKYOKU(self, tag, data):
        self.round.ryuukyoku = True
        if 'owari' in data:
            self.owari = data['owari']
        # For special ryuukyoku types, set to string ID rather than boolean
        if 'type' in data:
            self.round.ryuukyoku = data['type']
        if self.round.ryuukyoku is True or self.round.ryuukyoku == "nm":
            tenpai = self.round.ryuukyoku_tenpai = []
            for index, attr_name in enumerate(self.HANDS):
                if attr_name in data:
                    tenpai.append(index)

    def tagAGARI(self, tag, data):
        agari = Agari()
        self.round.agari.append(agari)
        agari.type = "RON" if data["fromWho"] != data["who"] else "TSUMO"
        agari.player = int(data["who"])
        agari.hand = self.decodeList(data["hai"], Tile)
        
        agari.fu, agari.points, limit = self.decodeList(data["ten"])
        if limit:
            agari.limit = self.LIMITS[limit]
        agari.dora = self.decodeList(data["doraHai"], Tile)
        agari.machi = self.decodeList(data["machi"], Tile)
        if "m" in data:
            agari.melds = self.decodeList(data["m"], Meld.decode)
            agari.closed = all(not hasattr(meld, "fromPlayer") for meld in agari.melds)
        else:
            agari.closed = True
        if "dorahaiUra" in data:
            agari.uradora = self.decodeList(data["uradoraHai"], Tile)
        if agari.type == "RON":
            agari.fromPlayer = int(data["fromWho"])
        if "yaku" in data:
            yakuList = self.decodeList(data["yaku"])
            agari.yaku = tuple((self.YAKU[yaku],han) for yaku,han in zip(yakuList[::2], yakuList[1::2]))
        elif "yakuman" in data:
            agari.yakuman = tuple(self.YAKU[yaku] for yaku in self.decodeList(data["yakuman"]))
        if 'owari' in data:
            self.owari = data['owari']

    @staticmethod
    def default(self, tag, data):
        if tag[0] in "DEFG":
            discard = Discard(self.round.events)
            discard.tile = Tile(tag[1:])
            discard.player = ord(tag[0]) - ord("D")
            discard.connected = self.players[discard.player].connected
        elif tag[0] in "TUVW":
            draw = Draw(self.round.events)
            draw.tile = Tile(tag[1:])
            draw.player = ord(tag[0]) - ord("T")
        else:
            pass

    @staticmethod
    def decodeList(list, dtype = int):
        return tuple(dtype(i) for i in list.split(","))

    def decode(self, log):
        events = etree.parse(log).getroot()
        self.rounds = []
        self.players = []
        for event in events:
            self.TAGS.get(event.tag, self.default)(self, event.tag, event.attrib)
        del self.round

for key in Game.__dict__:
    if key.startswith('tag'):
        Game.TAGS[key[3:]] = getattr(Game, key)

def tileToByte(t):
    if t[0].isdigit():
        tValue = int(t[0])
    else:
        # Avoiding White Drage & West Wind, so change to Bai Dragon.
        if t[1] == "d" and t[0] == "w":
            tValue = 6
        else:
            tValue = {"e": 1, "s": 2, "w": 3, "n": 4, "r": 5, "b": 6, "g": 7}[t[0]]
    tType = {"m": 0, "p": 1, "s": 2, "w": 3, "d": 3}[t[1]]
    tMeld = 0
    if len(t) > 2:
        tMeld = int(t[2])
    return tMeld << 6 | tType << 4 | tValue

def toMahjongHand(hand):
    retHand = []
    for i in hand:
        retHand.append(tileToByte(i))
    retHand.sort()
    return retHand

def expandHandToCSV(byteHand):
    retHand = []
    for i in byteHand:
        retHand += list(bin(i)[2:].zfill(8))
    return retHand

if __name__=='__main__':
    import yaml
    import sys
    for path in sys.argv[1:]:
        if path.isdigit():
            import os
            fullPath = os.path.dirname(os.path.abspath("__file__")) + "/mjlog_pf4-20_n" + path + "/"
            logs = os.listdir(fullPath)
            saveFeatureString = ""
            saveClassString = ""
            totalCount = len(logs)
            current = 0
            for log in logs:
                current += 1
                if current % 50 == 0:
                    print("Processed: " + str(current * 1.0 / totalCount * 100.0) + "%")
                fullLogPath = fullPath + log
                game = Game()
                try:
                    fo = open(fullLogPath)
                    game.decode(fo)
                    fo.close()
                except:
                    print("Error file: " + fullLogPath)
                    continue
                playerNO = int(fullLogPath[-1])
                resultDict = game.asdata()
                #yaml.dump(game.asdata(), sys.stdout, default_flow_style=False, allow_unicode=True)
                for round in resultDict["rounds"]:
                    playerHand = round["hands"][playerNO]
                    lastEvent = round["events"][0] # This is for identifying chi tile.
                    eventIndex = -1;
                    eventLength = len(round["events"]) - 1
                    validateEventIndex = 0
                    for event in round["events"]:
                        eventIndex += 1
                        if event["type"] == "Dora":
                            lastEvent = event
                            continue
                        if event["player"] == playerNO:
                            if event["type"] == "Draw":
                                playerHand.append(event["tile"])
                                if len(playerHand) != 14:
                                    raise ValueError("Player Hand length error: ", len(playerHand), playerHand)
                                playerHandInBytes = toMahjongHand(playerHand)
                                playerHandSplit = expandHandToCSV(playerHandInBytes)
                                if eventIndex != eventLength:
                                    saveFeatureString += ','.join(playerHandSplit) + '\n'
                                    validateEventIndex = eventIndex
                                    #print(eventIndex, ": Draw", event["tile"])
                            elif event["type"] == "Discard":
                                playerHand.remove(event["tile"])
                                if lastEvent["type"] == "Draw" or lastEvent["type"] == "Dora":
                                    saveClassString += ','.join(list(bin(tileToByte(event["tile"]))[2:].zfill(8))) + '\n'
                                    if lastEvent["type"] == "Dora":
                                        validateEventIndex += 1
                                    if validateEventIndex != eventIndex - 1:
                                        raise ValueError("Event index not match,", fullLogPath)
                                    #print(eventIndex - 1, ":Discard", event["tile"], "\n")
                            elif event["type"] == "Call":
                                meld = event["meld"]
                                if meld["type"] == "pon":
                                    playerHand.remove(meld["tiles"][0])
                                    playerHand.remove(meld["tiles"][0])
                                    playerHand.append(meld["tiles"][0] + "1")
                                    playerHand.append(meld["tiles"][0] + "1")
                                    playerHand.append(meld["tiles"][0] + "1")
                                elif meld["type"] == "kan" or meld["type"] == "chakan":
                                    if meld["tiles"][0]+"1" in playerHand:
                                        playerHand.remove(meld["tiles"][0]+"1")
                                        playerHand.remove(meld["tiles"][0]+"1")
                                        playerHand.remove(meld["tiles"][0]+"1")
                                    else:
                                        playerHand.remove(meld["tiles"][0])
                                        playerHand.remove(meld["tiles"][0])
                                        playerHand.remove(meld["tiles"][0])
                                    if meld["tiles"][0] in playerHand:
                                        playerHand.remove(meld["tiles"][0])
                                    playerHand.append(meld["tiles"][0] + "2")
                                    playerHand.append(meld["tiles"][0] + "2")
                                    playerHand.append(meld["tiles"][0] + "2")

                                    if lastEvent["player"] == playerNO and lastEvent["type"] == "Draw":
                                        saveFeatureString = saveFeatureString[:saveFeatureString.rfind('\n')]
                                        saveFeatureString = saveFeatureString[:saveFeatureString.rfind('\n')+1]
                                        #print("Removed Draw above.")
                                elif meld["type"] == "chi":
                                    for i in range(3):
                                        if meld["tiles"][i] != lastEvent["tile"]:
                                            playerHand.remove(meld["tiles"][i])
                                    playerHand.append(meld["tiles"][0] + "1")
                                    playerHand.append(meld["tiles"][1] + "1")
                                    playerHand.append(meld["tiles"][2] + "1")
                                else:
                                    raise ValueError("Unrecognised meld type: " + meld["type"])
                                #playerHandInBytes = toMahjongHand(playerHand)
                                #playerHandSplit = expandHandToCSV(playerHandInBytes)
                                #saveFeatureString += ','.join(playerHandSplit) + '\n'
                            else:
                                raise ValueError("Unrecognised event type!")
                        lastEvent = event
        featureFile = open(fullPath + "n" + path + "X.csv", "w+")
        featureFile.write(saveFeatureString)
        featureFile.close()
        classFile = open(fullPath + "n" + path + "y.csv", "w+")
        classFile.write(saveClassString)
        classFile.close()


