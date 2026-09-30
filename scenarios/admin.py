from django.contrib import admin

from .models import Battle, BattleOrbat, Exercise


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "exercise",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "exercise",
    )

    search_fields = (
        "name",
        "exercise__name",
    )


@admin.register(BattleOrbat)
class BattleOrbatAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "exercise_id",
        "battle_id",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "exercise_id",
        "battle_id",
    )

    search_fields = (
        "id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
