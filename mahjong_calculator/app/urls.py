from django.urls import path
from .import views

app_name="app"
urlpatterns = [
    path("", views.top, name="top"),
    path("new_calc", views.new_calc, name="new_calc"),
    path("score_calc/<int:game_id>/<str:round_hand>", views.score_calc, name="score_calc"),
    path("hand_calc", views.hand_calc, name="hand_calc"),
    path("manage_game/<int:game_id>", views.manage_game, name="manage_game"),
    path("show_ranking", views.show_ranking, name="show_ranking"),
    path("history_detail/<int:game_id>", views.history_detail, name="history_detail"),
]
