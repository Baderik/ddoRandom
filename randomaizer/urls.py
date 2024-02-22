from django.urls import path
from randomaizer.views import GameView

urlpatterns = [
    path("<int:gid>/", GameView.as_view())
]
