from django.urls import path

from . import views


urlpatterns = [
    path(
        "battle/<int:battle_id>/tick/",
        views.execute_battle_tick,
        name="execute_battle_tick",
    ),
]