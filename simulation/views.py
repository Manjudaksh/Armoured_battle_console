from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from scenarios.models import Battle
from simulation.models import Simulation
from simulation.services.engine import SimulationEngine


@login_required
@require_POST
def execute_battle_tick(request, battle_id):
    battle = get_object_or_404(Battle, pk=battle_id)

    simulation, created = Simulation.objects.get_or_create(
        battle=battle,
        defaults={
            "status": "CREATED",
            "current_tick": 0,
            "elapsed_seconds": 0,
        },
    )

    engine = SimulationEngine(simulation)

    try:
        if simulation.status == "CREATED":
            engine.start()
        elif simulation.status != "RUNNING":
            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        f"Simulation is not RUNNING. "
                        f"Current status: {simulation.status}"
                    ),
                },
                status=400,
            )

        result = engine.execute_tick()

        return JsonResponse(
            {
                "success": True,
                "battle_id": battle.id,
                "simulation_id": simulation.id,
                "simulation_status": simulation.status,
                "tick": result,
            }
        )

    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=500,
        )