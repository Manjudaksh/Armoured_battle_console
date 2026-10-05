from django.db import models


class Unit(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        DAMAGED = "DAMAGED", "Damaged"
        IMMOBILISED = "IMMOBILISED", "Immobilised"
        DESTROYED = "DESTROYED", "Destroyed"

    formation = models.ForeignKey(
        "formations.Formation",
        on_delete=models.CASCADE,
        related_name="units",
    )

    name = models.CharField(
        max_length=100,
    )

    platform = models.ForeignKey(
        "forces.Platform",
        on_delete=models.PROTECT,
        related_name="battle_units",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    ammunition = models.JSONField(
        default=dict,
        blank=True,
    )

    is_hvt = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["formation", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["formation", "name"],
                name="unique_unit_name_per_formation",
            ),
        ]

    def __str__(self):
        return f"{self.formation.name} - {self.name}"


class UnitState(models.Model):
    """
    Stores the current live battlefield state of a unit.

    This represents the latest state only.
    Historical states will be recorded separately by
    the simulation/tick and replay system.
    """

    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name="state",
    )

    # Geographic position
    latitude = models.FloatField(
        null=True,
        blank=True,
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
    )

    altitude = models.FloatField(
        null=True,
        blank=True,
    )

    # Movement state
    heading = models.FloatField(
        default=0.0,
        help_text="Heading in degrees.",
    )

    speed = models.FloatField(
        default=0.0,
        help_text="Current speed in metres per second.",
    )

    is_moving = models.BooleanField(
        default=False,
    )

    is_immobilised = models.BooleanField(
        default=False,
    )

    # Combat state
    health = models.FloatField(
        default=100.0,
    )

    morale = models.FloatField(
        default=100.0,
    )

    fuel = models.FloatField(
        default=100.0,
    )

    # Visibility/detection state
    is_detected = models.BooleanField(
        default=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"State - {self.unit.name}"


class UnitOrder(models.Model):
    class OrderType(models.TextChoices):
        MOVE = "MOVE", "Move"
        HOLD = "HOLD", "Hold"
        ATTACK = "ATTACK", "Attack"
        DEFEND = "DEFEND", "Defend"
        RECON = "RECON", "Recon"
        SUPPORT = "SUPPORT", "Support"
        WITHDRAW = "WITHDRAW", "Withdraw"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    order_type = models.CharField(
        max_length=20,
        choices=OrderType.choices,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    # Optional movement destination
    target_latitude = models.FloatField(
        null=True,
        blank=True,
    )

    target_longitude = models.FloatField(
        null=True,
        blank=True,
    )

    target_altitude = models.FloatField(
        null=True,
        blank=True,
    )

    # Optional target unit for attack/support/etc.
    target_unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="targeted_by_orders",
    )

    priority = models.PositiveIntegerField(
        default=1,
    )

    issued_at = models.DateTimeField(
        auto_now_add=True,
    )

    activated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    class Meta:
        ordering = ["-priority", "-issued_at"]

    def __str__(self):
        return f"{self.unit.name} - {self.order_type} - {self.status}"