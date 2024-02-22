from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404

from randomaizer.models import Game


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
        # game = get_object_or_404(Game, id=gid)

        return HttpResponse(get_client_ip(request))
