from django.forms import ModelForm
from .models import Game
from .models import Result


class Game_SettingForm(ModelForm):
    class Meta:
        model = Game
        fields = [
            "game_type",
            "player1",
            "player2",
            "player3",
            "player4",
            "default_score",
            "is_bankruptcy",
            "is_kuitan",
        ]


class Hand_calcForm(ModelForm):
    class Meta:
        model = Result
        fields = [
            "hand",
            "winner",
            "loser",
            "ready_player",
            "waiting_player",
            "pick",
            "ready",
            "closed_tile",
            "melted_tile",
            "win_tile",
            "dora"
        ]
