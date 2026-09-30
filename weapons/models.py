from django.db import models


class Weapon(models.Model):

    class WeaponClass(models.TextChoices):
        KINETIC = "KINETIC", "Kinetic"
        CHEMICAL = "CHEMICAL", "Chemical Energy"
        AUTOCANNON = "AUTOCANNON", "Autocannon"
        ARTILLERY = "ARTILLERY", "Artillery"
        MISSILE = "MISSILE", "Missile"
        MACHINE_GUN = "MACHINE_GUN", "Machine Gun"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    weapon_class = models.CharField(
        max_length=30,
        choices=WeaponClass.choices,
    )

    # ---------------------------------------------------------
    # Basic technical characteristics
    # ---------------------------------------------------------

    caliber_mm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    barrel_length_calibers = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    effective_range_m = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    maximum_range_m = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    rate_of_fire_rpm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    reload_time_seconds = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    # ---------------------------------------------------------
    # Fire-control characteristics
    # ---------------------------------------------------------

    stabilized = models.BooleanField(
        default=False,
    )

    fire_control_system = models.CharField(
        max_length=150,
        blank=True,
    )

    day_sight = models.BooleanField(
        default=False,
    )

    night_sight = models.BooleanField(
        default=False,
    )

    thermal_sight = models.BooleanField(
        default=False,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    source = models.ForeignKey(
        "forces.InventorySource",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="weapons",
    )

    source_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


class Ammunition(models.Model):

    class AmmunitionType(models.TextChoices):
        KINETIC = "KINETIC", "Kinetic"
        CHEMICAL = "CHEMICAL", "Chemical Energy"
        HE = "HE", "High Explosive"
        ATGM = "ATGM", "Anti-Tank Guided Missile"
        AP = "AP", "Armour Piercing"
        OTHER = "OTHER", "Other"

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    designation = models.CharField(
        max_length=150,
        blank=True,
    )

    ammunition_type = models.CharField(
        max_length=30,
        choices=AmmunitionType.choices,
    )

    caliber_mm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    source = models.ForeignKey(
        "forces.InventorySource",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ammunition",
    )

    source_notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class PlatformWeapon(models.Model):

    platform = models.ForeignKey(
        "forces.Platform",
        on_delete=models.CASCADE,
        related_name="platform_weapons",
    )

    weapon = models.ForeignKey(
        Weapon,
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
                fields=["platform", "weapon"],
                name="unique_weapon_per_platform",
            )
        ]

    def __str__(self):
        return f"{self.platform} - {self.weapon}"


class WeaponAmmunition(models.Model):

    weapon = models.ForeignKey(
        Weapon,
        on_delete=models.CASCADE,
        related_name="ammunition_types",
    )

    ammunition = models.ForeignKey(
        Ammunition,
        on_delete=models.PROTECT,
        related_name="weapons",
    )

    authorized_quantity = models.PositiveIntegerField(
        default=0,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["weapon", "ammunition"],
                name="unique_ammunition_per_weapon",
            )
        ]

    def __str__(self):
        return f"{self.weapon} - {self.ammunition}"
