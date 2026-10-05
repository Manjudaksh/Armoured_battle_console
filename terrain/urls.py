from django.urls import path

from terrain import views


urlpatterns = [
    path(
        "battle/<int:battle_id>/zones/",
        views.deployment_zones,
        name="deployment_zones",
    ),
    path(
        "battle/<int:battle_id>/zones/save/",
        views.save_deployment_zone,
        name="save_deployment_zone",
    ),
]