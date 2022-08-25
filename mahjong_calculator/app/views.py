from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Game
from .models import Hand
from .models import Result
from .forms import Game_SettingForm
from .forms import Hand_calcForm
from .calculator import PrintResult
from .manage_game import ManageGame, transform_hand_name, create_hand_data


# トップページ top.html を呼び出す処理
def top(request):
    context = {
        'tables' : Game.objects.all().order_by('-created_datetime')
    }

    return render(request, 'app/top.html', context)


# 入力画面 new_calc.html を呼び出す・保存する処理
def new_calc(request):

    if request.method == "POST":
        form = Game_SettingForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            game_id = Game.objects.latest('created_datetime').id
            round_hand = "1-0"
            
            # players_list = (
            #     ('player1', form.data.player1),
            #     ('player2', form.data.player2),
            #     ('player3', form.data.player3),
            #     ('player4', form.data.player4)
            # )

            return redirect('app:score_calc', game_id, round_hand)

    else:
        form = Game_SettingForm

        return render(request, 'app/new_calc.html', {'form':form})



# 入力画面 score_calc.html を呼び出す処理
def score_calc(request, game_id, round_hand):

    create_hand_data(game_id, round_hand)

    game = Game.objects.get(id=game_id)
    players = [game.player1, game.player2, game.player3, game.player4]

    context = {
        "form" : Hand_calcForm,
        "hand_id" : Hand.objects.order_by("id").last(),
        "hand_name" : transform_hand_name(round_hand),
        "players" : players
    }

    # context['win_form'].Meta.fields[1].choices = players_list
    # context['win_form'].meta.fields[2].choices = players_list

    return render(request, 'app/score_calc.html', context)


# Hand_calcForm を保存する処理
def hand_calc(request):

    print(request.POST)

    hand = Hand.objects.get(id=request.POST.hand_id)
    result = Result(hand = hand,
                count = hand.round_hand.split('-')[1],
                winner = request.POST.winner,
                loser = request.POST.loser)

    form = Hand_calcForm(request.POST)
    # print(form.data)
    hand_id = form.data["hand_id"]

    # if form.is_valid() == False:
        # for ele in form :
        #     print(ele)

    result = form.save(commit=False)
    result.hand = Hand.objects.get(id=hand_id)
    result.count = hand_id.split('-')[1]
    result.closed_tiles = form.data["input_tiles"]["closed"]
    result.melted_tiles = form.data["input_tiles"]["melted"]
    result.win_tile = form.data["input_tiles"]["win"]
    result.dora = form.data["input_tiles"]["dora"]

    if form.is_valid():
        print("aaaa")
        form.save()

        return redirect("app:manage_game", game_id)


# Hand テーブルをもとにデータを更新し、show_result を呼び出す処理
def manage_game(request, table_id):

    game = ManageGame(table_id)
    game.main()


    hand = Hand.objects.order_by('id').last()

    hand.hand_id = game.now_hand
    hand.save()


    # 和了した場合
    if hand.winner is not None:

        hand_id = hand.hand_id
        h_id = hand_id.split("-")

        if int(h_id[0]) <= 4:
            x = "東"
        else:
            x = "南"
        y = int(h_id[0]) % 4
        if y == 0:
            y = 4
        
        hand_id = x + str(y) + "局" + h_id[1] + "本場"

        context = {
            'table_id' : table_id,
            'hand_id' : hand_id,
            'hand' : hand
        }

        return render(request, 'app/show_result.html', context)
    
    else:

        return redirect('app:show_ranking')



# show_ranking を呼び出す処理
def show_ranking(request):

    table_id = Game.objects.latest('created_datetime').id

    game = ManageGame(table_id)
    game.get_data()
    game.manage_game()

    hand = Hand.objects.order_by('id').last()

    players = {
        game.p1_name : game.player1.score,
        game.p2_name : game.player2.score,
        game.p3_name : game.player3.score,
        game.p4_name : game.player4.score
    }
    players = sorted(players.items(), key=lambda x:x[1], reverse=True)

    hand_id = hand.hand_id
    h_id = hand_id.split("-")

    n_id = h_id


    if int(h_id[0]) <= 4:
        x = "東"
    else:
        x = "南"
    y = int(h_id[0]) % 4
    if y == 0:
        y = 4
    
    
    hand_id = x + str(y) + "局" + h_id[1] + "本場"


    if game.change_hand == "yes":
        n_id = str(int(n_id[0]) + 1) + "-0"
    else:
        n_id = str(n_id[0]) + "-" + str(int(n_id[1]) + 1)
    
    n_id = n_id.split("-")

    if int(n_id[0]) <= 4:
        z1 = "東"
    else:
        z1 = "南"
    z2 = int(n_id[0]) % 4
    if z2 == 0:
        z2 = 4
    

    next_id = z1 + str(z2) + "局" + n_id[1] + "本場"


    context = {
        'table_id' : table_id,
        'hand_id' : hand_id,
        'next_id' : next_id,
        'hand' : hand,
        'players' : players,
        'game_end' : game.game_end
    }

    return render(request, 'app/show_ranking.html', context)

    

# 履歴詳細画面 history_detail を呼び出す処理
def history_detail(request, table_id):

    hands = Hand.objects.all().filter(table = table_id)

    return render(request, 'app/history_detail.html', {'hands':hands})