from django.core.management.base import BaseCommand, CommandError

from scenarios.models import Battle
from simulation.services.initializer import BattleInitializer


class Command(BaseCommand):
    help = "Initialize UnitState records for a battle."

    def add_arguments(self, parser):
        parser.add_argument(
            "battle_id",
            type=int,
            help="ID of the battle to initialize.",
        )

    def handle(self, *args, **options):
        battle_id = options["battle_id"]

        try:
            battle = Battle.objects.get(
                pk=battle_id,
            )
        except Battle.DoesNotExist:
            raise CommandError(
                f"Battle with ID {battle_id} does not exist."
            )

        if battle.status == Battle.Status.RUNNING:
            raise CommandError(
                "Cannot initialize a battle that is already running."
            )

        initializer = BattleInitializer(battle)

        try:
            count = initializer.initialize()
        except ValueError as exc:
            raise CommandError(str(exc))

        self.stdout.write(
            self.style.SUCCESS(
                f"Battle '{battle.name}' initialized successfully. "
                f"{count} units initialized."
            )
        )