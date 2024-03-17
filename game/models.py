from django.db import models
from django.utils.translation import gettext_lazy as _


class Game(models.Model):
    start_dt = models.DateTimeField(_(u"Start Game Date and time"), auto_now_add=True, blank=True)
    end_dt = models.DateTimeField(_(u"End Game Date and time"), blank=True, null=True)
    traitors_count = models.PositiveIntegerField(_(u"Count of traitors in game"), default=0)
    traitors_max = models.PositiveIntegerField(_(u"Max count of traitors in game"), default=1)
    players_count = models.PositiveIntegerField(_(u"Count of players in game"), default=0)
    players_max = models.PositiveIntegerField(_(u"Max count of players in game"), default=2)


class Player(models.Model):
    ip = models.GenericIPAddressField(_(u'IP Address of player'), unique=True)


class GamePlayer(models.Model):
    # player = models.ForeignKey('Player', on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField(_(u'IP Address of player'), unique=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    is_traitor = models.BooleanField(_(u'Is imposter?'), default=False)
