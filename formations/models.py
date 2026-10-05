from django.db import models


class Formation(models.Model):
    class FormationType(models.TextChoices):
        ALPHA_ASSAULT = "ALPHA_ASSAULT", "ALPHA Assault"
        BRAVO_HVT_DEFENCE = "BRAVO_HVT_DEFENCE", "BRAVO HVT Defence"
        CHARLIE_FIRE_SUPPORT = "CHARLIE_FIRE_SUPPORT", "CHARLIE Fire Support"
        DELTA_RECON = "DELTA_RECON", "DELTA Recon"
        RED_ASSAULT = "RED_ASSAULT", "RED Assault"
        RED_DEFENCE = "RED_DEFENCE", "RED Defence"
        RED_FLANK = "RED_FLANK", "RED Flank"
        RED_SUPPORT = "RED_SUPPORT", "RED Support"

    class Doctrine(models.TextChoices):
        AGGRESSIVE = "AGGRESSIVE", "Aggressive"
        FLANKING = "FLANKING", "Flanking"
        SUPPRESSIVE = "SUPPRESSIVE", "Suppressive"
        DEFENSIVE = "DEFENSIVE", "Defensive"

    battle = models.ForeignKey(
        "scenarios.Battle",
        on_delete=models.CASCADE,
        related_name="formations",
    )

    battle_force = models.ForeignKey(
        "scenarios.BattleForce",
        on_delete=models.CASCADE,
        related_name="formations",
    )

    name = models.CharField(max_length=100)

    formation_type = models.CharField(
        max_length=40,
        choices=FormationType.choices,
    )

    doctrine = models.CharField(
        max_length=20,
        choices=Doctrine.choices,
        blank=True,
    )

    is_ai_controlled = models.BooleanField(default=False)

    is_ready = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["battle", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["battle", "name"],
                name="unique_formation_name_per_battle",
            ),
        ]

    def __str__(self):
        return f"{self.battle.name} - {self.name}"