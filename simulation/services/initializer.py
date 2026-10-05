from units.models import Unit, UnitState


class BattleInitializer:
    """
    Creates the initial live state for every unit participating
    in a battle.

    This does not start the simulation.

    Responsibilities:
        1. Find all units belonging to the battle.
        2. Find their BLUE/RED deployment zone.
        3. Calculate deterministic starting positions.
        4. Create or reset UnitState records.
    """

    def __init__(self, battle):
        self.battle = battle

    def initialize(self):
        """
        Initialize all units belonging to this battle.

        Returns:
            int: number of initialized units.
        """

        zones = {
            zone.side: zone
            for zone in self.battle.deployment_zones.filter(
                is_active=True,
            )
        }

        units = (
            Unit.objects
            .filter(
                formation__battle=self.battle,
            )
            .select_related(
                "formation",
                "formation__battle_force",
                "platform",
            )
        )

        initialized_count = 0

        side_counters = {
            "BLUE": 0,
            "RED": 0,
        }

        for unit in units:
            side = unit.formation.battle_force.side

            zone = zones.get(side)

            if zone is None:
                raise ValueError(
                    f"No active deployment zone exists for "
                    f"{side} in battle '{self.battle.name}'."
                )

            latitude, longitude = self._starting_position(
                zone,
                side_counters[side],
            )

            side_counters[side] += 1

            UnitState.objects.update_or_create(
                unit=unit,
                defaults={
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": 0.0,
                    "heading": self._starting_heading(side),
                    "speed": 0.0,
                    "health": 100.0,
                    "morale": 100.0,
                    "fuel": 100.0,
                    "is_detected": False,
                    "is_moving": False,
                    "is_immobilised": False,
                },
            )

            initialized_count += 1

        return initialized_count

    def _starting_position(self, zone, index):
        """
        Calculate a deterministic starting position inside
        the general area of the deployment polygon.

        Polygon format:

            [
                [longitude, latitude],
                [longitude, latitude],
                ...
            ]
        """

        polygon = zone.polygon

        if not polygon:
            raise ValueError(
                f"Deployment zone '{zone.name}' has no polygon."
            )

        if len(polygon) < 3:
            raise ValueError(
                f"Deployment zone '{zone.name}' must contain "
                f"at least three points."
            )

        longitudes = [point[0] for point in polygon]
        latitudes = [point[1] for point in polygon]

        min_longitude = min(longitudes)
        max_longitude = max(longitudes)

        min_latitude = min(latitudes)
        max_latitude = max(latitudes)

        center_longitude = (
            min_longitude + max_longitude
        ) / 2.0

        center_latitude = (
            min_latitude + max_latitude
        ) / 2.0

        # Small deterministic spacing between units.
        #
        # This is only initial placement.
        # Later the deployment system can use a proper
        # formation/deployment algorithm.
        spacing = 0.001

        row = index // 5
        column = index % 5

        longitude = (
            center_longitude
            + ((column - 2) * spacing)
        )

        latitude = (
            center_latitude
            + (row * spacing)
        )

        # Keep the generated point within the zone's
        # bounding box.
        longitude = max(
            min_longitude,
            min(longitude, max_longitude),
        )

        latitude = max(
            min_latitude,
            min(latitude, max_latitude),
        )

        return latitude, longitude

    def _starting_heading(self, side):
        """
        Initial facing direction.

        BLUE faces east.
        RED faces west.

        These are temporary defaults and will later be
        replaced by commander/AI deployment orientation.
        """

        if side == "BLUE":
            return 90.0

        return 270.0