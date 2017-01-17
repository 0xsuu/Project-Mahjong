# -*- coding: utf-8 -*-
import unittest

from tenhou.decoder import TenhouDecoder, Meld


class TenhouDecoderTestCase(unittest.TestCase):

    def test_parse_initial_round_values(self):
        decoder = TenhouDecoder()
        message = '<INIT seed="0,2,3,0,1,126" ten="250,250,250,250" oya="3" ' \
                  'hai="30,67,44,21,133,123,87,69,36,34,94,4,128"/>'

        values = decoder.parse_initial_values(message)
        self.assertEqual(values['round_number'], 0)
        self.assertEqual(values['count_of_honba_sticks'], 2)
        self.assertEqual(values['count_of_riichi_sticks'], 3)
        self.assertEqual(values['dora_indicator'], 126)
        self.assertEqual(values['dealer'], 3)

    def test_parse_initial_hand(self):
        decoder = TenhouDecoder()
        message = '<INIT seed="0,2,3,0,1,126" ten="250,250,250,250" oya="3" ' \
                  'hai="30,67,44,21,133,123,87,69,36,34,94,4,128"/>'
        tiles = decoder.parse_initial_hand(message)

        self.assertEqual(len(tiles), 13)

    def test_parse_initial_scores(self):
        decoder = TenhouDecoder()
        message = '<INIT seed="0,2,3,0,1,126" ten="240,260,270,280" oya="3" ' \
                  'hai="30,67,44,21,133,123,87,69,36,34,94,4,128"/>'
        values = decoder.parse_initial_values(message)

        self.assertEqual(values['scores'], [240, 260, 270, 280])

    def test_parse_names_and_ranks(self):
        decoder = TenhouDecoder()
        message = '<un n0="%4e%6f%4e%61%6d%65" n1="%6f%32%6f%32" n2="%73%68%69%6d%6d%6d%6d%6d"' \
                  ' n3="%e5%b7%9d%e6%b5%b7%e8%80%81" dan="0,7,12,1" ' \
                  'rate="1500.00,1421.91,1790.94,1532.23" sx="m,m,m,m"/>'
        values = decoder.parse_names_and_ranks(message)

        self.assertEqual(values[0], {'name': 'NoName', 'rank': TenhouDecoder.RANKS[0]})
        self.assertEqual(values[1], {'name': 'o2o2', 'rank': TenhouDecoder.RANKS[7]})
        self.assertEqual(values[2], {'name': 'shimmmmm', 'rank': TenhouDecoder.RANKS[12]})
        self.assertEqual(values[3], {'name': u'川海老', 'rank': TenhouDecoder.RANKS[1]})

    def test_parse_final_scores_and_uma(self):
        decoder = TenhouDecoder()
        message = '<agari ba="0,0" hai="12,13,41,46,51,78,80,84,98,101,105" m="51243" ' \
                  'machi="101" ten="30,1000,0" yaku="20,1" dorahai="89" who="2" fromwho="1" ' \
                  'sc="225,0,240,-10,378,10,157,0" owari="225,-17.0,230,3.0,388,48.0,157,-34.0" />'
        values = decoder.parse_final_scores_and_uma(message)

        self.assertEqual(values['scores'], [225, 230, 388, 157])
        self.assertEqual(values['uma'], [-17, 3, 48, -34])

        message = '<ryuukyoku ten="30,1000,0" sc="225,0,240,-10,378,10,157,0" ' \
                  'owari="225,-17.0,230,3.0,388,48.0,157,-34.0" />'
        values = decoder.parse_final_scores_and_uma(message)

        self.assertEqual(values['scores'], [225, 230, 388, 157])
        self.assertEqual(values['uma'], [-17, 3, 48, -34])

    def test_parse_log_link(self):
        decoder = TenhouDecoder()
        message = '<TAIKYOKU oya="1" log="2016031911gm-0001-0000-381f693b"/>'

        game_id, position = decoder.parse_log_link(message)

        self.assertEqual(game_id, '2016031911gm-0001-0000-381f693b')
        self.assertEqual(position, 3)

    def test_auth_message(self):
        decoder = TenhouDecoder()
        message = '<HELO uname="%4E%6F%4E%61%6D%65" auth="20160318-54ebe070" ratingscale=""/>'

        result = decoder.parse_auth_string(message)

        self.assertEqual(result, '20160318-54ebe070')

    def test_generate_auth_token(self):
        client = TenhouDecoder()

        string = '20160318-54ebe070'
        self.assertEqual(client.generate_auth_token(string), '20160318-72b5ba21')

        string = '20160319-5b859bb3'
        self.assertEqual(client.generate_auth_token(string), '20160319-9bc528f3')

    def test_decode_new_dora_indicator(self):
        decoder = TenhouDecoder()
        message = '<DORA hai="125" />'

        result = decoder.parse_dora_indicator(message)

        self.assertEqual(result, 125)

    def test_parse_called_pon(self):
        decoder = TenhouDecoder()
        meld = decoder.parse_meld('<N who="3" m="34314" />')

        self.assertEqual(meld.who, 3)
        self.assertEqual(meld.type, Meld.PON)
        self.assertEqual(meld.tiles, [89, 90, 91])

    def test_parse_called_kan(self):
        decoder = TenhouDecoder()
        meld = decoder.parse_meld('<N who="3" m="13825" />')

        self.assertEqual(meld.who, 3)
        self.assertEqual(meld.type, Meld.KAN)
        self.assertEqual(meld.tiles, [52, 53, 54, 55])

    def test_parse_called_chakan(self):
        decoder = TenhouDecoder()
        meld = decoder.parse_meld('<N who="3" m="18547" />')

        self.assertEqual(meld.who, 3)
        self.assertEqual(meld.type, Meld.CHAKAN)
        self.assertEqual(meld.tiles, [48, 49, 50, 51])

    def test_parse_called_chi(self):
        decoder = TenhouDecoder()
        meld = decoder.parse_meld('<N who="3" m="27031" />')

        self.assertEqual(meld.who, 3)
        self.assertEqual(meld.type, Meld.CHI)
        self.assertEqual(meld.tiles, [42, 44, 51])

    def test_parse_tile(self):
        decoder = TenhouDecoder()

        tile = decoder.parse_tile('<t23/>')
        self.assertEqual(tile, 23)

        tile = decoder.parse_tile('<e24/>')
        self.assertEqual(tile, 24)

        tile = decoder.parse_tile('<f25/>')
        self.assertEqual(tile, 25)

        tile = decoder.parse_tile('<g26/>')
        self.assertEqual(tile, 26)

        tile = decoder.parse_tile('<f23 t="4"/>')
        self.assertEqual(tile, 23)

    def test_parse_who_called_riichi(self):
        decoder = TenhouDecoder()

        who = decoder.parse_who_called_riichi('<REACH who="2" ten="255,216,261,258" step="2"/>')
        self.assertEqual(who, 2)
