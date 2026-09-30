from django.urls import path

from .views import (armoured_inventory, force_player_orbat)


urlpatterns = [
    path(
        "armoured-inventory/",
        armoured_inventory,
        name="armoured_inventory",
    ),
   
    path(
    "battle-orbat/<int:battle_id>/",
    force_player_orbat,
    name="force_player_orbat",
),
]