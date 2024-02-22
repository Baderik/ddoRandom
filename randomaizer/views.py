from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from randomaizer.models import Game, GamePlayer
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
    def get(request, gid):
        game = get_object_or_404(Game, id=gid)
        user_ip = get_client_ip(request)
        player = GamePlayer.objects.filter(ip=user_ip, game=game).first()
        if player:
            is_imposter = player.is_imposter
        else:
            if game.players_max == game.players_count:
                return render(request, "user_res.html", {
                    "res": "Прости, игра заполнена"
                })

            imposter_add_count = game.imposter_max - game.imposter_count
            player_add_count = game.players_max - game.players_count
            is_imposter = randrange(imposter_add_count + player_add_count) < imposter_add_count
            player = GamePlayer.objects.create(ip=user_ip, game=game, is_imposter=is_imposter)
            player.save()
            if is_imposter:
                game.imposter_count += 1
            game.players_count += 1
            game.save()
        if is_imposter:
            res = "Импостер"
        else:
            res = "Член экипажа"

        return render(request, "user_res.html", {
            "res": res
        })
