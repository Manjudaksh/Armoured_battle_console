from django.db import models


class Objective(models.Model):
    class Side(models.TextChoices):
        BLUE = "BLUE", "Blue"
        RED = "RED", "Red"

    class ObjectiveType(models.TextChoices):
        HVT = "HVT", "High Value Target"
        PRIMARY = "PRIMARY", "Primary Objective"
        SECONDARY = "SECONDARY", "Secondary Objective"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DAMAGED = "DAMAGED", "Damaged"
        DESTROYED = "DESTROYED", "Destroyed"
        COMPLETED = "COMPLETED", "Completed"

    battle = models.ForeignKey(
        "scenarios.Battle",
        on_delete=models.CASCADE,
        related_name="objectives",
    )

    unit = models.OneToOneField(
        "units.Unit",
        on_delete=models.PROTECT,
        related_name="objective",
        null=True,
        blank=True,
    )

    name = models.CharField(
        max_length=100,
    )

    side = models.CharField(
        max_length=10,
        choices=Side.choices,
    )

    objective_type = models.CharField(
        max_length=20,
        choices=ObjectiveType.choices,
        default=ObjectiveType.HVT,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    priority = models.PositiveIntegerField(
        default=1,
    )

    description = models.TextField(
        blank=True,
    )
    latitude = models.FloatField(
        null=True,
        blank=True,
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
    )

    altitude = models.FloatField(
        default=0.0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["battle", "side", "priority"]

    def __str__(self):
        return f"{self.battle.name} - {self.side} - {self.name}"
