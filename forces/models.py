from django.db import models
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Force(models.Model):

    class ForceType(models.TextChoices):
        ARMOURED = "ARMOURED", "Armoured"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="forces",
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    force_type = models.CharField(
        max_length=30,
        choices=ForceType.choices,
        default=ForceType.ARMOURED,
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["country", "code"],
                name="unique_force_code_per_country",
            )
        ]

        ordering = ["country", "name"]

    def __str__(self):
        return f"{self.country.name} - {self.name}"


class InventorySource(models.Model):
    """
    Records where master inventory / technical data came from.
    """

    name = models.CharField(max_length=200)

    url = models.URLField(blank=True)

    publication_date = models.DateField(
        null=True,
        blank=True,
    )

    accessed_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Platform(models.Model):

    class PlatformType(models.TextChoices):
        MBT = "MBT", "Main Battle Tank"
        IFV = "IFV", "Infantry Fighting Vehicle"
        APC = "APC", "Armoured Personnel Carrier"
        ATGM_CARRIER = "ATGM_CARRIER", "ATGM Carrier"
        MRAP = "MRAP", "Mine Resistant Ambush Protected"
        LIGHT_ARMOURED = "LIGHT_ARMOURED", "Light Armoured Vehicle"
        RECON = "RECON", "Reconnaissance"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    platform_type = models.CharField(
        max_length=30,
        choices=PlatformType.choices,
    )

    manufacturer = models.CharField(
        max_length=150,
        blank=True,
    )

    country_of_origin = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(blank=True)

    # ---------------------------------------------------------
    # Physical characteristics
    # ---------------------------------------------------------

    crew_size = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    passenger_capacity = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    length_m = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    width_m = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    height_m = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    combat_weight_tonnes = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # ---------------------------------------------------------
    # Mobility
    # ---------------------------------------------------------

    engine_power_kw = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    max_speed_kmh = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    operational_range_km = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    fuel_capacity_litres = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # ---------------------------------------------------------
    # Simulation characteristics
    # ---------------------------------------------------------

    mobility_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Simulation mobility category.",
    )

    amphibious = models.BooleanField(
        default=False,
    )

    night_capable = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(default=True)

    # ---------------------------------------------------------
    # Provenance
    # ---------------------------------------------------------

    source = models.ForeignKey(
        InventorySource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="platforms",
    )

    source_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["platform_type", "name"]

    def __str__(self):
        return self.name


class ForcePlatform(models.Model):

    force = models.ForeignKey(
        Force,
        on_delete=models.CASCADE,
        related_name="platform_inventory",
    )

    platform = models.ForeignKey(
        Platform,
        on_delete=models.PROTECT,
        related_name="force_inventory",
    )

    authorized_quantity = models.PositiveIntegerField(
        default=0,
    )

    is_available_for_scenario = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["force", "platform"],
                name="unique_platform_per_force",
            )
        ]

    def __str__(self):
        return (
            f"{self.force} - "
            f"{self.platform} "
            f"({self.authorized_quantity})"
        )


class PlatformProtection(models.Model):
    """
    Abstract protection model.

    We intentionally keep this simulation-oriented rather than
    encoding sensitive/non-public armour construction details.
    """

    platform = models.OneToOneField(
        Platform,
        on_delete=models.CASCADE,
        related_name="protection",
    )

    protection_class = models.CharField(
        max_length=50,
        blank=True,
    )

    front_class = models.CharField(
        max_length=50,
        blank=True,
    )

    side_class = models.CharField(
        max_length=50,
        blank=True,
    )

    rear_class = models.CharField(
        max_length=50,
        blank=True,
    )

    top_class = models.CharField(
        max_length=50,
        blank=True,
    )

    notes = models.TextField(blank=True)

    source = models.ForeignKey(
        InventorySource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.platform} Protection"


class Sensor(models.Model):

    class SensorType(models.TextChoices):
        OPTICAL = "OPTICAL", "Optical"
        THERMAL = "THERMAL", "Thermal"
        RADAR = "RADAR", "Radar"
        LASER = "LASER", "Laser"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    sensor_type = models.CharField(
        max_length=30,
        choices=SensorType.choices,
    )

    detection_range_m = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    identification_range_m = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    night_capable = models.BooleanField(
        default=False,
    )

    weather_degradation = models.BooleanField(
        default=False,
    )

    description = models.TextField(blank=True)

    source = models.ForeignKey(
        InventorySource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class PlatformSensor(models.Model):

    platform = models.ForeignKey(
        Platform,
        on_delete=models.CASCADE,
        related_name="platform_sensors",
    )

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.PROTECT,
        related_name="platforms",
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["platform", "sensor"],
                name="unique_sensor_per_platform",
            )
        ]

    def __str__(self):
        return f"{self.platform} - {self.sensor}"

class ForcePlayerAssignment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="force_assignments",
    )

    force = models.ForeignKey(
        Force,
        on_delete=models.CASCADE,
        related_name="player_assignments",
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "force"],
                name="unique_force_player_assignment",
            )
        ]
        ordering = ["user", "force"]

    def __str__(self):
        return f"{self.user} → {self.force}"

# Create your models here.
