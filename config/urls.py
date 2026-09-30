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
]