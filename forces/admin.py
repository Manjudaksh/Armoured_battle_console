from django.contrib import admin

from .models import (
    Country,
    Force,
    InventorySource,
    Platform,
    ForcePlatform,
    PlatformProtection,
    Sensor,
    PlatformSensor,
    ForcePlayerAssignment,
)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Force)
class ForceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
        "force_type",
        "is_active",
    )

    list_filter = (
        "country",
        "force_type",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(InventorySource)
class InventorySourceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "publication_date",
        "accessed_date",
        "is_active",
    )

    search_fields = (
        "name",
        "url",
    )


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "designation",
        "platform_type",
        "country_of_origin",
        "is_active",
    )

    list_filter = (
        "platform_type",
        "is_active",
    )

    search_fields = (
        "name",
        "designation",
        "manufacturer",
    )


@admin.register(ForcePlatform)
class ForcePlatformAdmin(admin.ModelAdmin):
    list_display = (
        "force",
        "platform",
        "authorized_quantity",
        "is_available_for_scenario",
    )

    list_filter = (
        "is_available_for_scenario",
        "force__country",
        "platform__platform_type",
    )

    search_fields = (
        "force__name",
        "platform__name",
    )


@admin.register(PlatformProtection)
class PlatformProtectionAdmin(admin.ModelAdmin):
    list_display = (
        "platform",
        "protection_class",
        "front_class",
        "side_class",
        "rear_class",
        "top_class",
    )

    search_fields = (
        "platform__name",
    )


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sensor_type",
        "night_capable",
        "weather_degradation",
    )

    list_filter = (
        "sensor_type",
        "night_capable",
    )

    search_fields = (
        "name",
    )


@admin.register(PlatformSensor)
class PlatformSensorAdmin(admin.ModelAdmin):
    list_display = (
        "platform",
        "sensor",
        "quantity",
        "is_primary",
    )

    list_filter = (
        "sensor__sensor_type",
        "is_primary",
    )

    search_fields = (
        "platform__name",
        "sensor__name",
    )
@admin.register(ForcePlayerAssignment)
class ForcePlayerAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "force",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
        "force",
    )

    search_fields = (
        "user__username",
        "user__email",
        "force__name",
    )