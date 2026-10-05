import math

from django.db import transaction

from simulation.models import Simulation, SimulationTick
from units.models import UnitOrder


class SimulationEngine:
    """
    Basic tick-based simulation engine.

    Current movement implementation:
    - executes pending MOVE orders
    - moves units toward their target
    - updates UnitState every tick
    - completes the order when the target is reached

    Terrain, slope, mobility restrictions, LOS, detection,
    and combat will be added as separate simulation systems.
    """

    # Temporary simulation fallback.
    # Platform.max_speed_kmh is currently NULL in the seeded inventory.
    DEFAULT_SPEED_MPS = 10.0

    EARTH_RADIUS_M = 6_371_000.0
    ARRIVAL_DISTANCE_M = 2.0

    def __init__(self, simulation):
        self.simulation = simulation
        self.battle = simulation.battle

    def start(self):
        if self.simulation.status in ["COMPLETED", "CANCELLED"]:
            raise ValueError(
                "A completed or cancelled simulation cannot be started."
            )

        self.simulation.status = "RUNNING"
        self.simulation.save(
            update_fields=["status", "updated_at"]
        )

    def execute_tick(self):
        """
        Execute exactly one simulation tick.
        """

        if self.simulation.status != "RUNNING":
            raise ValueError(
                "Simulation must be RUNNING before executing a tick."
            )

        tick_number = self.simulation.current_tick + 1

        tick_interval_seconds = (
            self.battle.tick_interval_ms / 1000.0
        )

        units_processed = 0
        events_created = 0
        movements_completed = 0

        with transaction.atomic():

            pending_orders = (
                UnitOrder.objects
                .select_related(
                    "unit",
                    "unit__platform",
                    "unit__state",
                )
                .filter(
                    unit__formation__battle=self.battle,
                    order_type="MOVE",
                    status__in=["PENDING", "ACTIVE"],
                )
                .order_by("priority", "id")
            )

            for order in pending_orders:

                unit = order.unit
                state = getattr(unit, "state", None)

                if state is None:
                    continue

                units_processed += 1

                # --------------------------------------------------
                # Stop movement for immobilised/destroyed units.
                # --------------------------------------------------

                if (
                    unit.status == "DESTROYED"
                    or state.is_immobilised
                ):
                    state.is_moving = False
                    state.save(
                        update_fields=["is_moving"]
                    )

                    if order.status == "ACTIVE":
                        order.status = "CANCELLED"
                        order.cancelled_at = self._now()
                        order.save(
                            update_fields=[
                                "status",
                                "cancelled_at",
                            ]
                        )

                    continue

                # --------------------------------------------------
                # Activate pending movement order.
                # --------------------------------------------------

                if order.status == "PENDING":
                    order.status = "ACTIVE"
                    order.activated_at = self._now()
                    order.save(
                        update_fields=[
                            "status",
                            "activated_at",
                        ]
                    )

                # --------------------------------------------------
                # Calculate distance to destination.
                # --------------------------------------------------

                distance_m = self._distance_m(
                    state.latitude,
                    state.longitude,
                    order.target_latitude,
                    order.target_longitude,
                )

                # --------------------------------------------------
                # Destination already reached.
                # --------------------------------------------------

                if distance_m <= self.ARRIVAL_DISTANCE_M:

                    state.latitude = order.target_latitude
                    state.longitude = order.target_longitude
                    state.altitude = order.target_altitude
                    state.speed = 0.0
                    state.is_moving = False

                    state.save(
                        update_fields=[
                            "latitude",
                            "longitude",
                            "altitude",
                            "speed",
                            "is_moving",
                        ]
                    )

                    order.status = "COMPLETED"
                    order.completed_at = self._now()
                    order.save(
                        update_fields=[
                            "status",
                            "completed_at",
                        ]
                    )

                    movements_completed += 1
                    continue

                # --------------------------------------------------
                # Determine movement speed.
                # --------------------------------------------------

                speed_mps = self._get_speed_mps(unit)

                if speed_mps <= 0:
                    state.is_moving = False
                    state.speed = 0.0

                    state.save(
                        update_fields=[
                            "is_moving",
                            "speed",
                        ]
                    )

                    continue

                # --------------------------------------------------
                # Distance travelled during this tick.
                # --------------------------------------------------

                travel_distance_m = (
                    speed_mps * tick_interval_seconds
                )

                # --------------------------------------------------
                # Do not overshoot destination.
                # --------------------------------------------------

                if travel_distance_m >= distance_m:

                    state.latitude = order.target_latitude
                    state.longitude = order.target_longitude
                    state.altitude = order.target_altitude
                    state.heading = self._bearing_degrees(
                        state.latitude,
                        state.longitude,
                        order.target_latitude,
                        order.target_longitude,
                    )
                    state.speed = 0.0
                    state.is_moving = False

                    state.save(
                        update_fields=[
                            "latitude",
                            "longitude",
                            "altitude",
                            "heading",
                            "speed",
                            "is_moving",
                        ]
                    )

                    order.status = "COMPLETED"
                    order.completed_at = self._now()
                    order.save(
                        update_fields=[
                            "status",
                            "completed_at",
                        ]
                    )

                    movements_completed += 1
                    continue

                # --------------------------------------------------
                # Calculate heading before changing position.
                # --------------------------------------------------

                heading = self._bearing_degrees(
                    state.latitude,
                    state.longitude,
                    order.target_latitude,
                    order.target_longitude,
                )

                # --------------------------------------------------
                # Move along the great-circle bearing.
                # --------------------------------------------------

                new_latitude, new_longitude = (
                    self._destination_point(
                        state.latitude,
                        state.longitude,
                        heading,
                        travel_distance_m,
                    )
                )

                state.latitude = new_latitude
                state.longitude = new_longitude
                state.heading = heading
                state.speed = speed_mps
                state.is_moving = True

                state.save(
                    update_fields=[
                        "latitude",
                        "longitude",
                        "heading",
                        "speed",
                        "is_moving",
                    ]
                )

            # ------------------------------------------------------
            # Record simulation tick.
            # ------------------------------------------------------

            SimulationTick.objects.create(
                simulation=self.simulation,
                tick_number=tick_number,
                elapsed_seconds=(
                    tick_number * tick_interval_seconds
                ),
                units_processed=units_processed,
                events_created=events_created,
                metadata={
                    "movements_completed": movements_completed,
                },
            )

            self.simulation.current_tick = tick_number
            self.simulation.elapsed_seconds = (
                tick_number * tick_interval_seconds
            )

            self.simulation.save(
                update_fields=[
                    "current_tick",
                    "elapsed_seconds",
                    "updated_at",
                ]
            )

        return {
            "tick_number": tick_number,
            "units_processed": units_processed,
            "events_created": events_created,
            "movements_completed": movements_completed,
        }

    def _get_speed_mps(self, unit):
        """
        Return the simulation movement speed.

        If the platform has a max_speed_kmh value, use it.
        Otherwise use the temporary simulation fallback.
        """

        max_speed_kmh = unit.platform.max_speed_kmh

        if max_speed_kmh is not None:
            return float(max_speed_kmh) / 3.6

        return self.DEFAULT_SPEED_MPS

    def _distance_m(
        self,
        latitude1,
        longitude1,
        latitude2,
        longitude2,
    ):
        """
        Haversine distance in metres.
        """

        lat1 = math.radians(latitude1)
        lat2 = math.radians(latitude2)

        delta_lat = math.radians(
            latitude2 - latitude1
        )

        delta_lon = math.radians(
            longitude2 - longitude1
        )

        a = (
            math.sin(delta_lat / 2) ** 2
            +
            math.cos(lat1)
            * math.cos(lat2)
            * math.sin(delta_lon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a),
        )

        return self.EARTH_RADIUS_M * c

    def _bearing_degrees(
        self,
        latitude1,
        longitude1,
        latitude2,
        longitude2,
    ):
        """
        Initial great-circle bearing in degrees.
        """

        lat1 = math.radians(latitude1)
        lat2 = math.radians(latitude2)

        delta_lon = math.radians(
            longitude2 - longitude1
        )

        x = (
            math.sin(delta_lon)
            * math.cos(lat2)
        )

        y = (
            math.cos(lat1)
            * math.sin(lat2)
            -
            math.sin(lat1)
            * math.cos(lat2)
            * math.cos(delta_lon)
        )

        bearing = math.degrees(
            math.atan2(x, y)
        )

        return (bearing + 360.0) % 360.0

    def _destination_point(
        self,
        latitude,
        longitude,
        bearing_degrees,
        distance_m,
    ):
        """
        Calculate a point reached by travelling a given distance
        along a great-circle bearing.
        """

        angular_distance = (
            distance_m / self.EARTH_RADIUS_M
        )

        bearing = math.radians(
            bearing_degrees
        )

        lat1 = math.radians(latitude)
        lon1 = math.radians(longitude)

        lat2 = math.asin(
            math.sin(lat1)
            * math.cos(angular_distance)
            +
            math.cos(lat1)
            * math.sin(angular_distance)
            * math.cos(bearing)
        )

        lon2 = (
            lon1
            +
            math.atan2(
                math.sin(bearing)
                * math.sin(angular_distance)
                * math.cos(lat1),
                math.cos(angular_distance)
                -
                math.sin(lat1)
                * math.sin(lat2),
            )
        )

        return (
            math.degrees(lat2),
            math.degrees(lon2),
        )

    @staticmethod
    def _now():
        from django.utils import timezone
        return timezone.now()