from django.urls import path

from . import views


urlpatterns = [
    path(
        "battle/<int:battle_id>/hvts/",
        views.battle_hvts,
        name="battle_hvts",
    ),
]