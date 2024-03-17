from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from game.models import Game, GamePlayer
from random import randrange


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class GameView(View):
    @staticmethod
    def get(request, gid: int):
        game = get_object_or_404(Game, id=gid)
        user_ip = get_client_ip(request)
        player = GamePlayer.objects.filter(ip=user_ip, game=game).first()
        if player:
            is_traitor = player.is_traitor
        else:
            if game.players_max == game.players_count:
                return render(request, "game_index.html", {
                    "game_id": gid,
                    "success": False,
                    "message": "Прости, игра заполнена"
                })

            available_number_traitors = game.traitors_max - game.traitors_count
            available_number_players = game.players_max - game.players_count
            is_traitor = (randrange(available_number_traitors + available_number_players)
                          < available_number_traitors)
            player = GamePlayer.objects.create(ip=user_ip, game=game, is_traitor=is_traitor)
            player.save()
            if is_traitor:
                game.traitors_count += 1
            game.players_count += 1
            game.save()

        if is_traitor:
            res = "Утка"
            text = ("Убивайте, перемещайтесь по карте,"
                    " устраивайте саботажи и делайте другие \"утиные\" вещи.")
            img_url = "duck.png"
        else:
            res = "Гусь"
            text = "Выполняйте задания, оставайтесь в живых и попробуйте выгнать уток голосованием."
            img_url = "goose.png"

        return render(request, "game_index.html", {
            "game_id": gid,
            "success": True,
            "role": res,
            "text": text,
            "img_url": img_url
        })
