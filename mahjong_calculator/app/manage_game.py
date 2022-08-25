# coding UTF-8
import sqlite3
from .models import Game
from .models import Hand

# DB よりデータを取得するクラス
class ConnectDB:

    def __init__(self, game):
        self.game = game
    

    # game テーブルより指定したデータを取得する関数
    def get_game(self):

        # DB へ接続
        dbname = "db.sqlite3"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        # データを返送（１件）
        cur.execute(f'SELECT * FROM app_game WHERE id = {self.game}')
        return cur.fetchone()


    # hand テーブルより指定したデータを取得する関数
    def get_hands(self):

        # DB へ接続
        dbname = "db.sqlite3"
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        # データを返送（全件）
        cur.execute(f'SELECT * FROM app_hand WHERE game_id = {self.game} ORDER BY id desc')
        return cur.fetchall()


# player テーブルより指定したデータを取得する関数
def get_player(p_id):

    # DB へ接続
    dbname = 'db.sqlite3'
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    # データを返送（１件）
    cur.execute(f'SELECT * FROM app_player WHERE id = {p_id}')
    return cur.fetchone()


# プレイヤーの情報を保持するクラス
class SettingPlayer:

    # 変数の初期化処理
    def __init__(self, seat):

        self.score = 25000      # プレイヤーの持ち点

        # プレイヤーの風
        if seat == 1:
            self.wind = "east"
        elif seat == 2:
            self.wind = "south"
        elif seat == 3:
            self.wind = "west"
        else:
            self.wind = "north"



# ゲームを進行するクラス
class ManageGame:

    # 変数の初期化処理
    def __init__(self, game_id):
        self.game_id = game_id        # 卓ID

        self.main()


    # メイン処理
    def main(self):
        
        self.get_data()
        # self.set_game()
    

    # DB からデータを取得する
    def get_data(self):
        
        db = ConnectDB(self.game_id)

        self.game = db.get_game()
        self.hands = db.get_hands()

        print(self.game)
        print(self.hands[0])


    # DB よりゲームの状態をセッティングする
    def set_game(self):

        self.game_type = self.game[1]  # 0:東風, 1:半荘
        self.default_score = self.game[6]
        self.players = [self.game[3], self.game[4], self.game[5], self.game[10]]

        before_hand = self.hands[1]
        now_hand = self.hands[0]

        if len(self.hands) >= 2:
            before_scores = [before_hand[9], before_hand[10], before_hand[11], before_hand[12]]
            before_deposit = before_hand[3]

        else:
            before_scores = [self.game[6], self.game[6], self.game[6], self.game[6]]
            before_deposit = 0
        
        is_win = True
        is_tsumo = False
        riichi_players = ""
        waiting_players = ""

        if now_hand[2] == None:
            is_win = False

        if now_hand[1] == None:
            is_tsumo = True
        
        if is_win:
            winner = now_hand[2]
            win_score = now_hand[8]
        
        if not is_tsumo:
            loser = now_hand[1]

        if not now_hand[5] == None:
            riichi_players = now_hand[5]
        
        if not now_hand[7] == None:
            waiting_players = now_hand[7]

    

    # 立直者のリー棒を回収する処理
    def collect_chips(self, player):

        if player == self.p1_name:
            self.player1.score -= 1000
        
        if player == self.p2_name:
            self.player2.score -= 1000
        
        if player == self.p3_name:
            self.player3.score -= 1000
        
        if player == self.p4_name:
            self.player4.score -= 1000
    

    # 点棒が増える処理
    def score_increase(self, player, cost):

        # プレイヤーがID指定でも名前指定でも統一する処理
        if type(player) is int:
            player_name = get_player(player)[1]
        else:
            player_name = player


        if player_name == self.p1_name:
            self.player1.score += cost
        
        if player_name == self.p2_name:
            self.player2.score += cost
        
        if player_name == self.p3_name:
            self.player3.score += cost
        
        if player_name == self.p4_name:
            self.player4.score += cost
    

    # 点棒が減る処理
    def score_decrease(self, player, cost):

        # プレイヤーがID指定でも名前指定でも統一する処理
        if type(player) is int:
            player_name = get_player(player)[1]
        else:
            player_name = player


        # ツモられた場合
        if self.tsumo == "yes":

            if player_name == self.p1_name:
                if self.player1.wind == "east":
                    self.player1.score -= int(cost / 2)
                else:
                    self.player1.score -= int(cost / 4)
            
            if player_name == self.p2_name:
                if self.player2.wind == "east":
                    self.player2.score -= int(cost / 2)
                else:
                    self.player2.score -= int(cost / 4)
            
            if player_name == self.p3_name:
                if self.player3.wind == "east":
                    self.player3.score -= int(cost / 2)
                else:
                    self.player3.score -= int(cost / 4)
            
            if player_name == self.p4_name:
                if self.player4.wind == "east":
                    self.player4.score -= int(cost / 2)
                else:
                    self.player4.score -= int(cost / 4)


        # ツモられ以外の場合
        else:

            if player_name == self.p1_name:
                self.player1.score -= cost
            
            if player_name == self.p2_name:
                self.player2.score -= cost
            
            if player_name == self.p3_name:
                self.player3.score -= cost
            
            if player_name == self.p4_name:
                self.player4.score -= cost
    

    # プレイヤーの風を確認し、返送する処理
    def check_wind(self, player):

        # プレイヤーがID指定でも名前指定でも統一する処理
        if type(player) is int:
            player_name = get_player(player)[1]
        else:
            player_name = player


        if player_name == self.p1_name:
            return self.player1.wind
        
        if player_name == self.p2_name:
            return self.player2.wind
        
        if player_name == self.p3_name:
            return self.player3.wind
        
        if player_name == self.p4_name:
            return self.player4.wind


    # プレイヤーの風を変更する処理
    def change_wind(self, hand):

        if int(hand) % 4 == 1:
            self.player1.wind = "east"
            self.player2.wind = "south"
            self.player3.wind = "west"
            self.player4.wind = "north"
        
        if int(hand) % 4 == 2:
            self.player1.wind = "north"
            self.player2.wind = "east"
            self.player3.wind = "south"
            self.player4.wind = "west"
        
        if int(hand) % 4 == 3:
            self.player1.wind = "west"
            self.player2.wind = "north"
            self.player3.wind = "east"
            self.player4.wind = "south"
        
        if int(hand) % 4 == 0:
            self.player1.wind = "south"
            self.player2.wind = "west"
            self.player3.wind = "north"
            self.player4.wind = "east"
            

    # メイン処理
    def manage_game(self):

        # プレイヤー４人のインスタンス化
        self.player1 = SettingPlayer(1)
        self.player2 = SettingPlayer(2)
        self.player3 = SettingPlayer(3)
        self.player4 = SettingPlayer(4)


        # 同卓のデータをループ処理
        for hand in self.hand_list:

            # 局・本場の移動の処理（東１局０本場以外の時だけ）
            if self.last_hand != "":
                
                # 前局から局が移った場合
                if self.change_hand == "yes":

                    l_hand = self.last_hand.split("-")
                    self.now_hand = str(int(l_hand[0]) + 1) + "-0"
                
                # 前局から本場が移った場合
                else:

                    l_hand = self.last_hand.split("-")
                    self.now_hand = str(l_hand[0]) + "-" + str(int(l_hand[1]) + 1)
            

            # 局に応じて風を移動させる処理
            n_hand = self.now_hand.split("-")
            self.change_wind(n_hand[0])


            hand_cont = 0           # 連荘変数 0なら次局へ

            self.tsumo  = "no"      # ツモ変数 yes ならツモ


            # 立直者が居た場合
            if hand[4] is not None:
                
                # 立直者が複数人の場合
                if ", " in hand[4]:
                    
                    riichi_players = hand[4].split(", ")        # 立直者リスト

                    for player in riichi_players:
                        self.collect_chips(player)              # リー棒回収
                    
                    self.chips += len(riichi_players) * 1000    # 場のリー棒を増やす
                
                # 立直者が一人の場合
                else:

                    self.collect_chips(hand[4])                 # リー棒回収

                    self.chips += 1000                          # 場のリー棒を増やす
            

            # 和了した場合
            if hand[8] is not None:

                # ツモの場合
                if hand[6] is None:


                    self.tsumo = "yes"
                    players = [self.p1_id, self.p2_id, self.p3_id, self.p4_id]  # プレイヤーリスト

                    self.score_increase(hand[8], hand[2])           # 和了点加算
                    self.score_increase(hand[8], self.chips)        # リー棒加算
                    self.chips = 0                                  # リー棒回収
                    players.remove(hand[8])

                    for player in players:
                        self.score_decrease(player, hand[2])        # ツモられ減算


                # ロンの場合
                else:

                    self.score_increase(hand[8], hand[2])           # 和了点加算
                    self.score_increase(hand[8], self.chips)        # リー棒加算
                    self.chips = 0                                  # リー棒回収

                    self.score_decrease(hand[6], hand[2])           # ツモられ減算


                # 親が和了した場合
                if self.check_wind(hand[8]) == "east":
                    hand_cont += 1                                  # 親和了チェック
            

            # 流局した場合
            else:

                # 聴牌者が居た場合
                if hand[5] is not None:

                    players = [self.p1_name, self.p2_name, self.p3_name, self.p4_name]  # プレイヤーリスト

                    # 聴牌者が複数人の場合
                    if ", " in hand[5]:

                        waiting_players = hand[5].split(", ")       # 聴牌者リスト
                        waiting_num = len(waiting_players)          # 聴牌の人数

                        in_cost = 3000 // waiting_num               # ノー点罰符（加算）
                        de_cost = 3000 // (4 - waiting_num)         # ノー点罰符（減算）
                        

                        # ノー点罰符（加算）処理
                        for player in waiting_players:
                            self.score_increase(player, in_cost)
                            players.remove(player)
                        
                        # ノー点罰符（減算）処理
                        for player in players:
                            self.score_decrease(player, de_cost)
                        
                        
                        # 親聴牌チェック
                        for player in waiting_players:
                            if self.check_wind(player) == "east":
                                hand_cont += 1
                    

                    # 聴牌者が一人の時
                    else:

                        # ノー点罰符（加算）処理
                        self.score_increase(hand[5], 3000)
                        players.remove(hand[5])

                        # ノー点罰符（減算）処理
                        for player in players:
                            self.score_decrease(player, 1000)


                        # 親聴牌チェック
                        if self.check_wind(hand[5]) == "east":
                            hand_cont += 1
            
            
            # last_hand 変数の更新（次局の為）
            self.last_hand = self.now_hand


            # 親の和了・聴牌に応じて change_hand 変数を更新
            if hand_cont == 0:
                self.change_hand = "yes"


            # 終局の判断をする処理
            # 東風戦の場合
            if self.game_type == 0:
                n_hand = self.now_hand.split("-")

                if int(n_hand[0]) >= 4 and self.change_hand == "yes":
                    self.game_end = "yes"
            
            # 東南戦の場合
            else:
                n_hand = self.now_hand.split("-")

                if int(n_hand[0]) >= 8 and self.change_hand == "yes":
                    self.game_end = "yes"
            

            # 飛び終局の判断をする処理
            score_list = [self.player1.score, self.player2.score, self.player3.score, self.player4.score]
            score_list.sort()

            if score_list[0] < 0:
                self.game_end = "yes"


def transform_hand_name(round_hand):

    round_hand = round_hand.split("-")
    num_hand = int(round_hand[0])
    num_count = int(round_hand[1])

    if num_hand <= 4:
        round_name = "東"
    elif num_hand <= 8:
        round_name = "南"
    elif num_hand <= 12:
        round_name = "西"
    else:
        round_name = "北"
    
    hand_name = num_hand % 4

    if hand_name == 0:
        hand_name = 4
    
    hand_name = f'{round_name}{hand_name}局{num_count}本場'

    return hand_name


def create_hand_data(game_id, round_hand):

    db = ConnectDB(game_id)

    game = db.get_game()
    hands = db.get_hands()

    # print(game)
    # print(hands)

    if len(hands) == 0:
        Hand.objects.create(
            game=Game(id=game[0]),
            round_hand=round_hand,
            player1_score=game[6],
            player2_score=game[6],
            player3_score=game[6],
            player4_score=game[6],
            deposit=0)
            