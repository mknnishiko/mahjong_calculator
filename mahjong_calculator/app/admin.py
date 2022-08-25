from django.contrib import admin
from .models import Result
from .models import Game
from .models import Hand


class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "game_type", "player1", "player2", "player3", "player4", "default_score", "is_bankruptcy", "is_kuitan", "created_datetime")

admin.site.register(Game, GameAdmin)


class HandAdmin(admin.ModelAdmin):
    list_display = ("id", "game", "round_hand", "player1_score", "player2_score", "player3_score", "player4_score", "deposit")

admin.site.register(Hand, HandAdmin)


class ResultAdmin(admin.ModelAdmin):
    list_display = ("hand", "count","winner", "loser", "ready_player", "waiting_player", "pick", "ready", "closed_tile", "melted_tile", "win_tile", "dora", "win_score", "condition")

admin.site.register(Result, ResultAdmin)
