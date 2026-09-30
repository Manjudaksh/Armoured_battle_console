from django.urls import path

from .views import (
    player_login,
    player_home,
    player_logout,
)


urlpatterns = [
    path(
        "login/",
        player_login,
        name="player_login",
    ),

    path(
        "home/",
        player_home,
        name="player_home",
    ),

    path(
        "logout/",
        player_logout,
        name="player_logout",
    ),
]