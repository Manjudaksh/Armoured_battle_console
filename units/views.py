import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from scenarios.models import Battle
from units.models import Unit, UnitOrder


@login_required
@require_GET
def battle_units(request, battle_id):
    battle = get_object_or_404(
        Battle,
        pk=battle_id
    )

    units = (
        Unit.objects
        .filter(
            formation__battle=battle
        )
        .select_related(
            "formation",
            "formation__battle_force",
            "platform",
            "state",
        )
    )

    data = []

    for unit in units:
        state = getattr(unit, "state", None)

        if state is None:
            continue

        data.append({
            "id": unit.id,
            "name": unit.name,
            "side": unit.formation.battle_force.side,
            "formation": unit.formation.name,
            "platform": unit.platform.name,

            "latitude": state.latitude,
            "longitude": state.longitude,
            "altitude": state.altitude,
            "heading": state.heading,
            "speed": state.speed,

            "health": state.health,
            "morale": state.morale,
            "fuel": state.fuel,

            "moving": state.is_moving,
            "immobilised": state.is_immobilised,
            "is_detected": state.is_detected,

            "is_hvt": unit.is_hvt,
        })

    return JsonResponse({
        "battle_id": battle.id,
        "units": data,
    })


@login_required
@require_POST
def move_unit(request, battle_id, unit_id):
    """
    Create a MOVE order for a battle unit.

    The simulation engine will execute this order later.
    """

    battle = get_object_or_404(
        Battle,
        pk=battle_id
    )

    unit = get_object_or_404(
        Unit.objects.select_related(
            "formation",
            "formation__battle_force",
            "state",
        ),
        pk=unit_id,
        formation__battle=battle,
    )

    try:
        payload = json.loads(
            request.body.decode("utf-8")
        )
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON request.",
            },
            status=400,
        )

    try:
        latitude = float(payload["latitude"])
        longitude = float(payload["longitude"])
        altitude = float(
            payload.get(
                "altitude",
                unit.state.altitude or 0
            )
        )
    except (KeyError, TypeError, ValueError):
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "latitude and longitude are required "
                    "and must be numeric."
                ),
            },
            status=400,
        )

    if not -90 <= latitude <= 90:
        return JsonResponse(
            {
                "success": False,
                "error": "Latitude must be between -90 and 90.",
            },
            status=400,
        )

    if not -180 <= longitude <= 180:
        return JsonResponse(
            {
                "success": False,
                "error": "Longitude must be between -180 and 180.",
            },
            status=400,
        )

    # Do not allow a new movement order for a destroyed unit.
    if unit.status == Unit.Status.DESTROYED:
        return JsonResponse(
            {
                "success": False,
                "error": "Destroyed units cannot receive movement orders.",
            },
            status=400,
        )

    # Cancel any previous pending/active MOVE orders.
    UnitOrder.objects.filter(
        unit=unit,
        order_type="MOVE",
        status__in=["PENDING", "ACTIVE"],
    ).update(
        status="CANCELLED"
    )

    order = UnitOrder.objects.create(
        unit=unit,
        order_type="MOVE",
        status="PENDING",
        target_latitude=latitude,
        target_longitude=longitude,
        target_altitude=altitude,
        priority=1,
        metadata={
            "source": "player_map_command",
        },
    )

    return JsonResponse({
        "success": True,
        "message": "MOVE order created.",
        "battle_id": battle.id,
        "unit_id": unit.id,
        "unit_name": unit.name,
        "order": {
            "id": order.id,
            "type": order.order_type,
            "status": order.status,
            "target_latitude": order.target_latitude,
            "target_longitude": order.target_longitude,
            "target_altitude": order.target_altitude,
        },
    })