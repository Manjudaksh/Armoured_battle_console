from django.db import models


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Battle(models.Model):
    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        ORBAT_SETUP = "ORBAT_SETUP", "ORBAT Setup"
        READY = "READY", "Ready"
        RUNNING = "RUNNING", "Running"
        COMPLETED = "COMPLETED", "Completed"

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="battles",
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.PLANNED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.exercise.name} - {self.name}"


class BattleForce(models.Model):
    """
    Defines which force participates in a battle
    and which side it belongs to.
    """

    class Side(models.TextChoices):
        BLUE = "BLUE", "Blue"
        RED = "RED", "Red"

    battle = models.ForeignKey(
        Battle,
        on_delete=models.CASCADE,
        related_name="battle_forces",
    )

    force = models.ForeignKey(
        "forces.Force",
        on_delete=models.PROTECT,
        related_name="battle_participations",
    )

    side = models.CharField(
        max_length=10,
        choices=Side.choices,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["battle", "force"],
                name="unique_force_per_battle",
            ),
        ]
        ordering = ["battle", "side", "force"]

    def __str__(self):
        return f"{self.battle.name} - {self.force.name} - {self.side}"


class BattleOrbat(models.Model):
    """
    Stores the ORBAT snapshot for one battle.

    master_orbat:
        Snapshot of the available force data for the battle.

    playing_orbat:
        Actual platforms selected for the battle.
    """

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="battle_orbats",
    )
    battle = models.OneToOneField(
        Battle,
        on_delete=models.CASCADE,
        related_name="orbat",
    )

    master_orbat = models.JSONField(
        default=dict,
        blank=True,
    )

    playing_orbat = models.JSONField(
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Battle ORBAT - {self.battle.name}"