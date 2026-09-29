from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from config import settings



@login_required
def dashboard(request):
    return render(
        request,
        "admin/dashboard.html",
        {"cesium_ion_token": settings.CESIUM_ION_TOKEN}
    )