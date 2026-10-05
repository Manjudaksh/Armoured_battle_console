from django.urls import path

from units import views


urlpatterns = [
    path(
        "battle/<int:battle_id>/",
        views.battle_units,
        name="battle_units",
    ),
    path(
        "battle/<int:battle_id>/unit/<int:unit_id>/move/",
        views.move_unit,
        name="move_unit",
    ),
]