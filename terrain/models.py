from django.db import models


class BattleTerrain(models.Model):
    """
    Terrain configuration used by a specific battle.

    The actual 3D terrain and imagery are provided by Cesium.
    This model stores the configuration needed by our application.
    """

    battle = models.OneToOneField(
        "scenarios.Battle",
        on_delete=models.CASCADE,
        related_name="terrain",
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    # Cesium ion asset IDs.
    terrain_asset_id = models.CharField(
        max_length=100,
        blank=True,
    )

    imagery_asset_id = models.CharField(
        max_length=100,
        blank=True,
    )

    # Geographic area used by the exercise.
    # Values are in decimal degrees.
    min_longitude = models.FloatField(
        null=True,
        blank=True,
    )

    min_latitude = models.FloatField(
        null=True,
        blank=True,
    )

    max_longitude = models.FloatField(
        null=True,
        blank=True,
    )

    max_latitude = models.FloatField(
        null=True,
        blank=True,
    )

    # Optional terrain metadata.
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.battle.name} - {self.name}"


class DeploymentZone(models.Model):
    """
    Deployment area for one side of a battle.

    The polygon is stored as JSON in longitude/latitude form.

    Example:
    [
        [74.10, 32.10],
        [74.30, 32.10],
        [74.30, 32.30],
        [74.10, 32.30]
    ]
    """

    class Side(models.TextChoices):
        BLUE = "BLUE", "Blue"
        RED = "RED", "Red"

    battle = models.ForeignKey(
        "scenarios.Battle",
        on_delete=models.CASCADE,
        related_name="deployment_zones",
    )

    side = models.CharField(
        max_length=10,
        choices=Side.choices,
    )

    name = models.CharField(
        max_length=100,
    )

    polygon = models.JSONField(
        default=list,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["battle", "side", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["battle", "side"],
                name="unique_deployment_zone_per_side",
            ),
        ]

    def __str__(self):
        return f"{self.battle.name} - {self.side} - {self.name}"