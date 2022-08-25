from django.db import models
from django.forms import BooleanField

GAME_TYPE_CHOICES = (
    (0, "東風戦"),
    (1, "半荘戦")
)

PICK_CHOICES = (
    (0, "ツモ"),
    (1, "ロン"),
    (2, "嶺上開花"),
    (3, "海底撈月"),
    (4, "河底撈魚"),
    (5, "搶槓"),
    (6, "流し満貫"),
    (7, "天和・地和")
)

READY_CHOICES = (
    (0, "立直"),
    (1, "立直一発"),
    (2, "ダブル立直"),
    (3, "ダブル立直一発")
)

class Game(models.Model):
    game_type = models.IntegerField(choices=GAME_TYPE_CHOICES)
    player1 = models.CharField(max_length=10, null=False, blank=False)
    player2 = models.CharField(max_length=10, null=False, blank=False)
    player3 = models.CharField(max_length=10, null=False, blank=False)
    player4 = models.CharField(max_length=10, null=False, blank=False)
    default_score = models.IntegerField(null=False, blank=False, default=25000)
    is_bankruptcy = models.BooleanField(default=True)
    is_kuitan = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Hand(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    round_hand = models.CharField(max_length=5, default="1-0")
    player1_score = models.IntegerField(null=False, blank=False, default=25000)
    player2_score = models.IntegerField(null=False, blank=False, default=25000)
    player3_score = models.IntegerField(null=False, blank=False, default=25000)
    player4_score = models.IntegerField(null=False, blank=False, default=25000)
    deposit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.id)




class Result(models.Model):
    hand = models.OneToOneField(Hand, on_delete=models.CASCADE, primary_key=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    winner = models.CharField(max_length=10, null=True, blank=True)
    loser = models.CharField(max_length=10, null=True, blank=True)
    ready_player = models.CharField(max_length=10, null=True, blank=True)
    waiting_player = models.CharField(max_length=10, null=True, blank=True)
    pick = models.IntegerField(choices=PICK_CHOICES, null=True, blank=True)
    ready = models.IntegerField(choices=READY_CHOICES, null=True, blank=True)
    closed_tile = models.CharField(max_length=50, null=True, blank=True)
    melted_tile = models.CharField(max_length=50, null=True, blank=True)
    win_tile = models.CharField(max_length=5, null=True, blank=True)
    dora = models.CharField(max_length=50, null=True, blank=True)
    win_tile = models.CharField(max_length=5, null=True, blank=True)
    dora = models.CharField(max_length=20, null=True, blank=True)
    win_score = models.IntegerField(blank=True, null=True, default=0)
    condition = models.CharField(max_length=100, blank=True, null=True)

    def ___str___(self):
        return self.win_score
