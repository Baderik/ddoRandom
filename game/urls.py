from django.urls import path
from game.views import GameView

urlpatterns = [
    path("<int:gid>/", GameView.as_view())
]
