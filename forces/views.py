from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import (
    Country,
    Force,
    ForcePlatform,
     ForcePlayerAssignment
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import  redirect
from scenarios.models import Battle, BattleOrbat




@staff_member_required
def armoured_inventory(request):

    countries = Country.objects.filter(
        is_active=True
    ).order_by("name")

    selected_country_id = request.GET.get("country")
    selected_force_id = request.GET.get("force")

    selected_country = None
    selected_force = None
    inventory = []

    # ---------------------------------------------------------
    # COUNTRY
    # ---------------------------------------------------------

    if selected_country_id:
        selected_country = get_object_or_404(
            Country,
            id=selected_country_id,
            is_active=True,
        )

    # ---------------------------------------------------------
    # FORCES
    # ---------------------------------------------------------

    forces = Force.objects.filter(
        is_active=True,
    ).select_related(
        "country",
    ).order_by(
        "name",
    )

    if selected_country:
        forces = forces.filter(
            country=selected_country,
        )

    # ---------------------------------------------------------
    # SELECTED FORCE
    # ---------------------------------------------------------

    if selected_force_id:
        selected_force = get_object_or_404(
            Force.objects.select_related("country"),
            id=selected_force_id,
            is_active=True,
        )

        inventory = ForcePlatform.objects.filter(
            force=selected_force,
            platform__is_active=True,
        ).select_related(
            "platform",
            "platform__source",
        ).prefetch_related(
            "platform__platform_weapons__weapon",
            "platform__platform_sensors__sensor",
        ).order_by(
            "platform__platform_type",
            "platform__name",
        )

    context = {
        "countries": countries,
        "forces": forces,
        "selected_country": selected_country,
        "selected_force": selected_force,
        "inventory": inventory,
    }

    return render(
        request,
        "forces/armoured_inventory.html",
        context,
    )
    
@login_required
def force_player_orbat(request, battle_id):

    # ---------------------------------------------------------
    # 1. Find the forces assigned to the logged-in player
    # ---------------------------------------------------------

    assignments = ForcePlayerAssignment.objects.filter(
        user=request.user,
        is_active=True,
    ).select_related(
        "force",
        "force__country",
    )

    if not assignments.exists():
        messages.error(
            request,
            "You are not assigned to an active force.",
        )

        return redirect("player_home")

    assigned_forces = [
        assignment.force
        for assignment in assignments
    ]


    # ---------------------------------------------------------
    # 2. Find the selected Battle
    # ---------------------------------------------------------

    from scenarios.models import Battle, BattleOrbat

    battle = get_object_or_404(
        Battle,
        pk=battle_id,
    )


    # ---------------------------------------------------------
    # 3. Find the Battle ORBAT belonging to this Battle
    # ---------------------------------------------------------

    orbat = get_object_or_404(
        BattleOrbat,
        battle_id=battle.id,
    )


    # =========================================================
    # GET
    # =========================================================

    if request.method == "GET":

        force_id = request.GET.get("force")

        selected_force = None
        inventory = []

        if force_id:

            selected_force = next(
                (
                    force
                    for force in assigned_forces
                    if str(force.id) == str(force_id)
                ),
                None,
            )

            if selected_force:

                inventory = (
                    ForcePlatform.objects
                    .filter(
                        force=selected_force,
                        is_available_for_scenario=True,
                        platform__is_active=True,
                    )
                    .select_related(
                        "platform",
                        "platform__source",
                    )
                    .prefetch_related(
                        "platform__platform_weapons__weapon",
                        "platform__platform_sensors__sensor",
                    )
                    .order_by(
                        "platform__platform_type",
                        "platform__name",
                    )
                )

        return render(
            request,
            "forces/force_player_orbat.html",
            {
                "battle": battle,
                "orbat": orbat,
                "assignments": assignments,
                "selected_force": selected_force,
                "inventory": inventory,
            },
        )


    # =========================================================
    # POST
    # =========================================================

    if request.method == "POST":

        force_id = request.POST.get("force_id")

        # -----------------------------------------------------
        # 4. Confirm that this force belongs to this player
        # -----------------------------------------------------

        selected_force = next(
            (
                force
                for force in assigned_forces
                if str(force.id) == str(force_id)
            ),
            None,
        )

        if not selected_force:

            messages.error(
                request,
                "You are not authorized to use this force.",
            )

            return redirect(
                "force_player_orbat",
                battle_id=battle.id,
            )


        # -----------------------------------------------------
        # 5. Load only authorized inventory
        # -----------------------------------------------------

        authorized_inventory = {
            str(item.id): item
            for item in (
                ForcePlatform.objects
                .filter(
                    force=selected_force,
                    is_available_for_scenario=True,
                    platform__is_active=True,
                )
                .select_related("platform")
            )
        }


        # -----------------------------------------------------
        # 6. Validate selected quantities
        # -----------------------------------------------------

        selected_platforms = []

        for inventory_id, inventory_item in authorized_inventory.items():

            field_name = f"quantity_{inventory_id}"

            raw_quantity = request.POST.get(
                field_name,
                "0",
            )

            try:
                quantity = int(raw_quantity)

            except (TypeError, ValueError):

                messages.error(
                    request,
                    f"Invalid quantity for "
                    f"{inventory_item.platform.name}.",
                )

                return redirect(
                    "force_player_orbat",
                    battle_id=battle.id,
                )


            if quantity < 0:

                messages.error(
                    request,
                    f"Quantity cannot be negative: "
                    f"{inventory_item.platform.name}.",
                )

                return redirect(
                    "force_player_orbat",
                    battle_id=battle.id,
                )


            if quantity > inventory_item.authorized_quantity:

                messages.error(
                    request,
                    f"{inventory_item.platform.name}: "
                    f"maximum authorized quantity is "
                    f"{inventory_item.authorized_quantity}.",
                )

                return redirect(
                    "force_player_orbat",
                    battle_id=battle.id,
                )


            if quantity > 0:

                selected_platforms.append(
                    {
                        "force_platform_id": inventory_item.id,
                        "platform_id": inventory_item.platform.id,
                        "platform_name": inventory_item.platform.name,
                        "platform_type": inventory_item.platform.platform_type,
                        "quantity": quantity,
                    }
                )


        # -----------------------------------------------------
        # 7. Save the ORBAT snapshot
        # -----------------------------------------------------

        with transaction.atomic():

            current_master_orbat = (
                orbat.master_orbat or {}
            )

            current_playing_orbat = (
                orbat.playing_orbat or {}
            )


            # ---------------------------------------------
            # Master inventory snapshot
            # ---------------------------------------------

            master_forces = []

            for inventory_item in authorized_inventory.values():

                master_forces.append(
                    {
                        "force_platform_id": inventory_item.id,
                        "platform_id": inventory_item.platform.id,
                        "platform_name": inventory_item.platform.name,
                        "platform_type": inventory_item.platform.platform_type,
                        "authorized_quantity": inventory_item.authorized_quantity,
                    }
                )


            current_master_orbat["blue_land"] = {
                "force_id": selected_force.id,
                "force_name": selected_force.name,
                "country": selected_force.country.name,
                "forces": master_forces,
            }


            # ---------------------------------------------
            # Actual player selection
            # ---------------------------------------------

            current_playing_orbat["blue_land"] = {
                "force_id": selected_force.id,
                "force_name": selected_force.name,
                "country": selected_force.country.name,
                "selected_forces": selected_platforms,
            }


            # ---------------------------------------------
            # Save
            # ---------------------------------------------

            orbat.master_orbat = current_master_orbat

            orbat.playing_orbat = current_playing_orbat

            orbat.save(
                update_fields=[
                    "master_orbat",
                    "playing_orbat",
                    "updated_at",
                ]
            )


        # -----------------------------------------------------
        # 8. IMPORTANT: return a response after POST
        # -----------------------------------------------------

        messages.success(
            request,
            "Battle ORBAT saved successfully.",
        )
        return redirect(
            f"{reverse('force_player_orbat', kwargs={'battle_id': battle.id})}"
            f"?force={selected_force.id}"
        )


    # ---------------------------------------------------------
    # 9. Safety fallback
    # ---------------------------------------------------------

    return redirect(
        "force_player_orbat",
        battle_id=battle.id,
    )