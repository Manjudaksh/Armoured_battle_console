from django.db import models


class Simulation(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        RUNNING = "RUNNING", "Running"
        PAUSED = "PAUSED", "Paused"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    battle = models.OneToOneField(
        "scenarios.Battle",
        on_delete=models.CASCADE,
        related_name="simulation",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )

    current_tick = models.PositiveBigIntegerField(
        default=0,
    )

    elapsed_seconds = models.FloatField(
        default=0.0,
    )

    started_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    paused_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Simulation - {self.battle.name}"


class SimulationTick(models.Model):
    """
    Represents one deterministic simulation step.

    Example:

        tick_number = 1
        elapsed_seconds = 1.0

        tick_number = 2
        elapsed_seconds = 2.0
    """

    simulation = models.ForeignKey(
        Simulation,
        on_delete=models.CASCADE,
        related_name="ticks",
    )

    tick_number = models.PositiveBigIntegerField()

    elapsed_seconds = models.FloatField()

    processed_at = models.DateTimeField(
        auto_now_add=True,
    )

    # Summary information for this tick.
    units_processed = models.PositiveIntegerField(
        default=0,
    )

    events_created = models.PositiveIntegerField(
        default=0,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["tick_number"]

        constraints = [
            models.UniqueConstraint(
                fields=["simulation", "tick_number"],
                name="unique_tick_per_simulation",
            ),
        ]

    def __str__(self):
        return (
            f"{self.simulation.battle.name} "
            f"- Tick {self.tick_number}"
        )