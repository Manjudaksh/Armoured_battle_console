from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from scenarios.models import Battle
from objectives.models import Objective


@login_required
@require_GET
def battle_hvts(request, battle_id):
    battle = get_object_or_404(Battle, pk=battle_id)

    objectives = Objective.objects.filter(
        battle=battle,
        objective_type="HVT",
    ).order_by("side", "id")

    data = []

    for objective in objectives:
        data.append({
            "id": objective.id,
            "name": objective.name,
            "side": objective.side,
            "latitude": objective.latitude,
            "longitude": objective.longitude,
            "altitude": objective.altitude,
            "status": objective.status,
            "priority": objective.priority,
            "description": objective.description,
        })

    return JsonResponse({
        "battle_id": battle.id,
        "hvts": data,
    })
