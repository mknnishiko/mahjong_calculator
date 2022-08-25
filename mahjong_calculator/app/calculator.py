# coding UTF-8

from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.constants import EAST, SOUTH, WEST, NORTH


calculator = HandCalculator()


def print_hand_result(hand_result):
    print(hand_result.cost)
    print(hand_result.yaku)


# 手牌の文字列をtilesの引数の形に変換するクラス
class PrepareHand:


    input_hand = ""


    def __init__(self, val):
        self.input_hand = val


    man = ""
    pin = ""
    sou = ""
    honors = ""


    def sort_tiles(self):

        hand_array = self.input_hand.split()

        for tile in hand_array:
            if tile[1] == "m":
                PrepareHand.man += tile[0]
            elif tile[1] == "p":
                PrepareHand.pin += tile[0]
            elif tile[1] == "s":
                PrepareHand.sou += tile[0]
            else:
                PrepareHand.honors += tile[0]


# 結果を出力するクラス（引数に 手牌、和了り牌 を求める）
class PrintResult:

    cost = ""
    yaku = ""

    def __init__(self, hand, win_tile, dora, tsumo, riichi):
        
        hand = PrepareHand(hand)

        hand.sort_tiles()
        tiles = TilesConverter.string_to_136_array(man = hand.man, pin = hand.pin, sou = hand.sou, honors = hand.honors)

        if win_tile[1] == "m":
            win_tile = TilesConverter.string_to_136_array(man = win_tile[0])[0]
        elif win_tile[1] == "p":
            win_tile = TilesConverter.string_to_136_array(pin = win_tile[0])[0]
        elif win_tile[1] == "s":
            win_tile = TilesConverter.string_to_136_array(sou = win_tile[0])[0]
        else:
            win_tile = TilesConverter.string_to_136_array(honors = win_tile[0])[0]
        
        melds = None

        if dora[1] == "m":
            dora_indicators = TilesConverter.string_to_136_array(man = dora[0])[0]
        elif dora[1] == "p":
            dora_indicators = TilesConverter.string_to_136_array(pin = dora[0])[0]
        elif dora[1] == "s":
            dora_indicators = TilesConverter.string_to_136_array(sou = dora[0])[0]
        else:
            dora_indicators = TilesConverter.string_to_136_array(honors = dora[0])[0]

        config = HandConfig(is_tsumo = tsumo, is_riichi = riichi)

        result = calculator.estimate_hand_value(tiles, win_tile, melds, dora_indicators, config)

        
        self.cost = result.cost
        self.yaku = result.yaku


# a = PrintResult("1m 1m 1m 1p 1p 1p 1s 1s 1s 1h 1h 1h 5h 5h", "1m")

# print(a.cost)
# print(a.yaku)
