import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from scenarios.models import Battle
from terrain.models import DeploymentZone


@login_required
@require_GET
def deployment_zones(request, battle_id):
    battle = get_object_or_404(Battle, pk=battle_id)

    zones = []

    for zone in battle.deployment_zones.filter(is_active=True):
        zones.append(
            {
                "side": zone.side,
                "name": zone.name,
                "polygon": zone.polygon,
            }
        )

    return JsonResponse(
        {
            "battle_id": battle.id,
            "zones": zones,
        }
    )


@login_required
@require_POST
def save_deployment_zone(request, battle_id):
    battle = get_object_or_404(Battle, pk=battle_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Request body must contain valid JSON."},
            status=400,
        )

    side = data.get("side")
    polygon = data.get("polygon")

    valid_sides = {
        DeploymentZone.Side.BLUE,
        DeploymentZone.Side.RED,
    }

    if side not in valid_sides:
        return JsonResponse(
            {"error": "Side must be BLUE or RED."},
            status=400,
        )

    if not isinstance(polygon, list) or len(polygon) < 3:
        return JsonResponse(
            {"error": "Polygon must contain at least 3 points."},
            status=400,
        )

    cleaned_polygon = []

    for point in polygon:
        if (
            not isinstance(point, list)
            or len(point) != 2
        ):
            return JsonResponse(
                {
                    "error": (
                        "Each polygon point must be "
                        "[longitude, latitude]."
                    )
                },
                status=400,
            )

        try:
            longitude = float(point[0])
            latitude = float(point[1])
        except (TypeError, ValueError):
            return JsonResponse(
                {"error": "Polygon coordinates must be numbers."},
                status=400,
            )

        if not -180 <= longitude <= 180:
            return JsonResponse(
                {"error": "Longitude must be between -180 and 180."},
                status=400,
            )

        if not -90 <= latitude <= 90:
            return JsonResponse(
                {"error": "Latitude must be between -90 and 90."},
                status=400,
            )

        cleaned_polygon.append(
            [longitude, latitude]
        )

    zone, _ = DeploymentZone.objects.update_or_create(
        battle=battle,
        side=side,
        defaults={
            "name": f"{side} Deployment Zone",
            "polygon": cleaned_polygon,
            "is_active": True,
        },
    )

    return JsonResponse(
        {
            "success": True,
            "battle_id": battle.id,
            "side": zone.side,
            "name": zone.name,
            "polygon": zone.polygon,
        }
    )
