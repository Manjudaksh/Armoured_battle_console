from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Battle, BattleOrbat, Exercise


@staff_member_required
def battle_list(request):
    battles = (
        Battle.objects
        .select_related("exercise")
        .order_by("-created_at")
    )

    exercises = Exercise.objects.filter(
        is_active=True
    ).order_by("name")

    return render(
        request,
        "scenarios/battle_list.html",
        {
            "battles": battles,
            "exercises": exercises,
        },
    )


@staff_member_required
def create_battle(request):
    if request.method != "POST":
        return redirect("battle_list")

    exercise_id = request.POST.get("exercise_id")
    name = request.POST.get("name", "").strip()
    description = request.POST.get("description", "").strip()

    if not exercise_id:
        messages.error(request, "Please select an exercise.")
        return redirect("battle_list")

    if not name:
        messages.error(request, "Battle name is required.")
        return redirect("battle_list")

    exercise = get_object_or_404(
        Exercise,
        id=exercise_id,
        is_active=True,
    )

    battle = Battle.objects.create(
        exercise=exercise,
        name=name,
        description=description,
        status=Battle.Status.ORBAT_SETUP,
    )

    # Automatically create the Battle ORBAT.
    BattleOrbat.objects.create(
        exercise_id=exercise.id,
        battle_id=battle.id,
        master_orbat={},
        playing_orbat={},
    )

    messages.success(
        request,
        f"Battle '{battle.name}' created successfully.",
    )

    return redirect("battle_list")