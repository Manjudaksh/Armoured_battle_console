from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("django-admin/", admin.site.urls),

    path(
        "",
        include("admin_panel.urls"),
    ),
    path(
        "inventory/",
        include("forces.urls"),
    ),
    path(
    "",
    include("accounts.urls"),
    
),
    path("scenarios/", include("scenarios.urls")),
    path("terrain/", include("terrain.urls")),
    path("units/", include("units.urls")),
    path("simulation/", include("simulation.urls")),
    path("objectives/", include("objectives.urls")),
]