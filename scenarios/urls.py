from django.urls import path

from .views import battle_list, create_battle


urlpatterns = [
    path(
        "battles/",
        battle_list,
        name="battle_list",
    ),
    path(
        "battles/create/",
        create_battle,
        name="create_battle",
    ),
]