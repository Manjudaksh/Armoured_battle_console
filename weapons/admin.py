from django.contrib import admin

from .models import (
    Weapon,
    Ammunition,
    PlatformWeapon,
    WeaponAmmunition,
)


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "designation",
        "weapon_class",
        "caliber_mm",
        "effective_range_m",
        "maximum_range_m",
        "is_active",
    )

    list_filter = (
        "weapon_class",
        "is_active",
    )

    search_fields = (
        "name",
        "designation",
    )


@admin.register(Ammunition)
class AmmunitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "designation",
        "ammunition_type",
        "caliber_mm",
        "is_active",
    )

    list_filter = (
        "ammunition_type",
        "is_active",
    )

    search_fields = (
        "name",
        "designation",
    )


@admin.register(PlatformWeapon)
class PlatformWeaponAdmin(admin.ModelAdmin):
    list_display = (
        "platform",
        "weapon",
        "quantity",
        "is_primary",
    )

    list_filter = (
        "weapon__weapon_class",
        "is_primary",
    )

    search_fields = (
        "platform__name",
        "weapon__name",
    )


@admin.register(WeaponAmmunition)
class WeaponAmmunitionAdmin(admin.ModelAdmin):
    list_display = (
        "weapon",
        "ammunition",
        "authorized_quantity",
        "is_primary",
    )

    list_filter = (
        "ammunition__ammunition_type",
        "is_primary",
    )

    search_fields = (
        "weapon__name",
        "ammunition__name",
    )