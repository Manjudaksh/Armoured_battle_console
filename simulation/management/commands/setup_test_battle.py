from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from forces.models import Force, ForcePlatform, Platform
from scenarios.models import Battle, BattleForce
from formations.models import Formation
from units.models import Unit
from terrain.models import DeploymentZone


class Command(BaseCommand):
    help = "Create the initial test battle structure."

    @transaction.atomic
    def handle(self, *args, **options):
        # ---------------------------------------------------------
        # 1. Get the existing test battle
        # ---------------------------------------------------------

        try:
            battle = Battle.objects.get(pk=1)
        except Battle.DoesNotExist:
            raise CommandError(
                "Battle with ID 1 does not exist."
            )

        if battle.status != Battle.Status.PLANNED:
            raise CommandError(
                f"Battle '{battle.name}' is not PLANNED. "
                f"Current status: {battle.status}"
            )

        # ---------------------------------------------------------
        # 2. Get existing BLUE BattleForce
        # ---------------------------------------------------------

        blue_battle_force = (
            BattleForce.objects
            .filter(
                battle=battle,
                side=BattleForce.Side.BLUE,
                is_active=True,
            )
            .select_related("force")
            .first()
        )

        if blue_battle_force is None:
            raise CommandError(
                "No active BLUE BattleForce exists."
            )

        blue_force = blue_battle_force.force
        country = blue_force.country

        # ---------------------------------------------------------
        # 3. Create RED simulation force
        # ---------------------------------------------------------

        red_force, created = Force.objects.get_or_create(
            country=country,
            code="RED-SIM-01",
            defaults={
                "name": "Red Exercise Force",
                "force_type": Force.ForceType.ARMOURED,
                "description": (
                    "Synthetic RED force used for the "
                    "armoured battle simulation."
                ),
                "is_active": True,
            },
        )

        if not created:
            red_force.name = "Red Exercise Force"
            red_force.force_type = Force.ForceType.ARMOURED
            red_force.is_active = True

            red_force.save(
                update_fields=[
                    "name",
                    "force_type",
                    "is_active",
                ]
            )

        # ---------------------------------------------------------
        # 4. Copy available platform authorization
        # ---------------------------------------------------------

        blue_inventory = (
            ForcePlatform.objects
            .filter(
                force=blue_force,
                is_available_for_scenario=True,
            )
            .select_related("platform")
        )

        for inventory_item in blue_inventory:
            ForcePlatform.objects.update_or_create(
                force=red_force,
                platform=inventory_item.platform,
                defaults={
                    "authorized_quantity": (
                        inventory_item.authorized_quantity
                    ),
                    "is_available_for_scenario": True,
                },
            )

        # ---------------------------------------------------------
        # 5. Create RED BattleForce
        # ---------------------------------------------------------

        red_battle_force, _ = (
            BattleForce.objects.get_or_create(
                battle=battle,
                force=red_force,
                defaults={
                    "side": BattleForce.Side.RED,
                    "is_active": True,
                },
            )
        )

        if red_battle_force.side != BattleForce.Side.RED:
            red_battle_force.side = BattleForce.Side.RED
            red_battle_force.is_active = True

            red_battle_force.save(
                update_fields=[
                    "side",
                    "is_active",
                ]
            )

        # ---------------------------------------------------------
        # 6. Create BLUE formations
        # ---------------------------------------------------------

        blue_formations = [
            (
                "ALPHA Assault",
                Formation.FormationType.ALPHA_ASSAULT,
                False,
                "",
            ),
            (
                "BRAVO HVT Defence",
                Formation.FormationType.BRAVO_HVT_DEFENCE,
                False,
                Formation.Doctrine.DEFENSIVE,
            ),
            (
                "CHARLIE Fire Support",
                Formation.FormationType.CHARLIE_FIRE_SUPPORT,
                False,
                Formation.Doctrine.SUPPRESSIVE,
            ),
            (
                "DELTA Recon",
                Formation.FormationType.DELTA_RECON,
                False,
                Formation.Doctrine.DEFENSIVE,
            ),
        ]

        created_blue_formations = []

        for (
            name,
            formation_type,
            ai_controlled,
            doctrine,
        ) in blue_formations:

            formation, _ = Formation.objects.get_or_create(
                battle=battle,
                name=name,
                defaults={
                    "battle_force": blue_battle_force,
                    "formation_type": formation_type,
                    "doctrine": doctrine,
                    "is_ai_controlled": ai_controlled,
                    "is_ready": False,
                },
            )

            created_blue_formations.append(formation)

        # ---------------------------------------------------------
        # 7. Create RED AI formation
        # ---------------------------------------------------------

        red_formation, _ = Formation.objects.get_or_create(
            battle=battle,
            name="RED AI Main Force",
            defaults={
                "battle_force": red_battle_force,
                "formation_type": Formation.FormationType.RED_ASSAULT,
                "doctrine": Formation.Doctrine.AGGRESSIVE,
                "is_ai_controlled": True,
                "is_ready": False,
            },
        )

        # ---------------------------------------------------------
        # 8. Get existing platform inventory
        # ---------------------------------------------------------

        platforms = {
            platform.name: platform
            for platform in Platform.objects.all()
        }

        # ---------------------------------------------------------
        # 9. BLUE unit plan
        # ---------------------------------------------------------

        blue_unit_plan = {
            "ALPHA Assault": [
                ("ALPHA-01", "Bhishma"),
                ("ALPHA-02", "Bhishma"),
                ("ALPHA-03", "Ajeya Mk.2"),
                ("ALPHA-04", "Ajeya Mk.2"),
            ],
            "BRAVO HVT Defence": [
                ("BRAVO-01", "Arjun Mk.1"),
                ("BRAVO-02", "Arjun Mk.1"),
            ],
            "CHARLIE Fire Support": [
                ("CHARLIE-01", "Sarath"),
                ("CHARLIE-02", "Sarath"),
            ],
            "DELTA Recon": [
                ("DELTA-01", "Kestrel"),
                ("DELTA-02", "Kestrel"),
            ],
        }

        # ---------------------------------------------------------
        # 10. Create BLUE units
        # ---------------------------------------------------------

        for formation in created_blue_formations:
            planned_units = blue_unit_plan.get(
                formation.name,
                [],
            )

            for unit_name, platform_name in planned_units:
                platform = platforms.get(platform_name)

                if platform is None:
                    raise CommandError(
                        f"Platform '{platform_name}' does not exist."
                    )

                Unit.objects.get_or_create(
                    formation=formation,
                    name=unit_name,
                    defaults={
                        "platform": platform,
                        "status": Unit.Status.ACTIVE,
                        "ammunition": {},
                        "is_hvt": False,
                    },
                )

        # ---------------------------------------------------------
        # 11. RED unit plan
        # ---------------------------------------------------------

        red_unit_plan = [
            ("RED-01", "Bhishma"),
            ("RED-02", "Bhishma"),
            ("RED-03", "Ajeya Mk.2"),
            ("RED-04", "Sarath"),
            ("RED-05", "Kestrel"),
        ]

        # ---------------------------------------------------------
        # 12. Create RED units
        # ---------------------------------------------------------

        for unit_name, platform_name in red_unit_plan:
            platform = platforms.get(platform_name)

            if platform is None:
                raise CommandError(
                    f"Platform '{platform_name}' does not exist."
                )

            Unit.objects.get_or_create(
                formation=red_formation,
                name=unit_name,
                defaults={
                    "platform": platform,
                    "status": Unit.Status.ACTIVE,
                    "ammunition": {},
                    "is_hvt": False,
                },
            )

        # ---------------------------------------------------------
        # 13. Create BLUE deployment zone
        # ---------------------------------------------------------

        DeploymentZone.objects.get_or_create(
            battle=battle,
            side=DeploymentZone.Side.BLUE,
            defaults={
                "name": "BLUE Deployment Zone",
                "polygon": [],
                "is_active": True,
            },
        )

        # ---------------------------------------------------------
        # 14. Create RED deployment zone
        # ---------------------------------------------------------

        DeploymentZone.objects.get_or_create(
            battle=battle,
            side=DeploymentZone.Side.RED,
            defaults={
                "name": "RED Deployment Zone",
                "polygon": [],
                "is_active": True,
            },
        )

        # ---------------------------------------------------------
        # 15. Build summary values
        # ---------------------------------------------------------

        blue_formation_count = Formation.objects.filter(
            battle=battle,
            battle_force=blue_battle_force,
        ).count()

        red_formation_count = Formation.objects.filter(
            battle=battle,
            battle_force=red_battle_force,
        ).count()

        unit_count = Unit.objects.filter(
            formation__battle=battle,
        ).count()

        deployment_zone_count = DeploymentZone.objects.filter(
            battle=battle,
        ).count()

        # ---------------------------------------------------------
        # 16. Output summary
        # ---------------------------------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                "Test battle structure created successfully."
            )
        )

        self.stdout.write(
            f"Battle: {battle.id} - {battle.name}"
        )

        self.stdout.write(
            f"BLUE Force: {blue_force.name}"
        )

        self.stdout.write(
            f"RED Force: {red_force.name}"
        )

        self.stdout.write(
            f"BLUE formations: {blue_formation_count}"
        )

        self.stdout.write(
            f"RED formations: {red_formation_count}"
        )

        self.stdout.write(
            f"Units: {unit_count}"
        )

        self.stdout.write(
            f"Deployment zones: {deployment_zone_count}"
        )