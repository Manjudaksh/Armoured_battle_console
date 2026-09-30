from django.db import models

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

class BattleOrbat(models.Model):
    """
    Stores the ORBAT snapshot for one battle.

    master_orbat:
        Snapshot of the available force data when the battle ORBAT
        is created.

    playing_orbat:
        The actual platforms selected for this battle.
    """

    exercise_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the exercise associated with this ORBAT.",
    )

    battle_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="ID of the battle associated with this ORBAT.",
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
        return f"Battle ORBAT #{self.pk}"