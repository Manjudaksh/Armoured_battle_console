from datetime import date

from django.core.management.base import BaseCommand

from forces.models import (
    Country,
    Force,
    InventorySource,
    Platform,
    ForcePlatform,
    PlatformProtection,
    Sensor,
    PlatformSensor,
)

from weapons.models import (
    Weapon,
    Ammunition,
    PlatformWeapon,
    WeaponAmmunition,
)


class Command(BaseCommand):
    help = "Seed Indian armoured master inventory."

    SOURCE_NAME = "Warpower India - Indian Land Power"
    SOURCE_URL = "https://www.warpowerindia.com/landpower.php"

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.WARNING(
                "=============================================="
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "  INDIAN ARMOURED MASTER INVENTORY SEED"
            )
        )
        self.stdout.write(
            self.style.WARNING(
                "=============================================="
            )
        )
        self.stdout.write("")

        # =========================================================
        # 1. SOURCE
        # =========================================================

        source, _ = InventorySource.objects.update_or_create(
            name=self.SOURCE_NAME,
            defaults={
                "url": self.SOURCE_URL,
                "accessed_date": date.today(),
                "notes": (
                    "Public-source inventory reference used for "
                    "the Indian armoured master dataset. "
                    "Inventory figures are source-reported and "
                    "should not be interpreted as authoritative "
                    "operational availability."
                ),
                "is_active": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"[SOURCE] {source.name}"
            )
        )

        # =========================================================
        # 2. COUNTRY
        # =========================================================

        india, _ = Country.objects.update_or_create(
            code="IN",
            defaults={
                "name": "India",
                "is_active": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "[COUNTRY] India"
            )
        )

        # =========================================================
        # 3. FORCE
        # =========================================================

        indian_armoured, _ = Force.objects.update_or_create(
            country=india,
            code="IN-ARMOURED",
            defaults={
                "name": "Indian Armoured Force",
                "force_type": Force.ForceType.ARMOURED,
                "description": (
                    "Indian armoured master inventory used by "
                    "the Armoured Battle Console."
                ),
                "is_active": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "[FORCE] Indian Armoured Force"
            )
        )

        # =========================================================
        # 4. PLATFORM MASTER DATA
        #
        # Only source-supported values are populated.
        # Unknown values remain NULL.
        # =========================================================

        platforms_data = [

            # -----------------------------------------------------
            # MBTs
            # -----------------------------------------------------

            {
                "key": "T72_AJEYA",
                "name": "Ajeya Mk.2",
                "designation": "T-72 Ajeya",
                "platform_type": Platform.PlatformType.MBT,

                "manufacturer": "India",
                "country_of_origin": "India / Soviet origin",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_MBT",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian modernization of the T-72 main battle "
                    "tank. Warpower India lists 2,410 units and "
                    "describes a 125mm smoothbore main gun with "
                    "autoloader."
                ),

                "quantity": 2410,

                "protection_class": "MBT",
                "front_class": "MBT_FRONT",
                "side_class": "MBT_SIDE",
                "rear_class": "MBT_REAR",
                "top_class": "MBT_TOP",
            },

            {
                "key": "T90S_BHISHMA",
                "name": "Bhishma",
                "designation": "T-90S Bhishma",
                "platform_type": Platform.PlatformType.MBT,

                "manufacturer": "India / Russian origin",
                "country_of_origin": "Russia / India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_MBT",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian T-90S main battle tank variant. "
                    "Warpower India lists 2,078 units and "
                    "describes a 125mm main gun with autoloader."
                ),

                "quantity": 2078,

                "protection_class": "MBT",
                "front_class": "MBT_FRONT",
                "side_class": "MBT_SIDE",
                "rear_class": "MBT_REAR",
                "top_class": "MBT_TOP",
            },

            {
                "key": "ARJUN_MK1",
                "name": "Arjun Mk.1",
                "designation": "Arjun",
                "platform_type": Platform.PlatformType.MBT,

                "manufacturer": "India",
                "country_of_origin": "India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_MBT",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian main battle tank. Warpower India "
                    "lists 124 units and identifies its main "
                    "gun as a 120mm rifled gun."
                ),

                "quantity": 124,

                "protection_class": "MBT",
                "front_class": "MBT_FRONT",
                "side_class": "MBT_SIDE",
                "rear_class": "MBT_REAR",
                "top_class": "MBT_TOP",
            },

            {
                "key": "ARJUN_MK1A",
                "name": "Arjun Mk.1A",
                "designation": "Arjun Mk.1A",
                "platform_type": Platform.PlatformType.MBT,

                "manufacturer": "India",
                "country_of_origin": "India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_MBT",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Improved Arjun main battle tank variant."
                ),

                "quantity": 2,

                "protection_class": "MBT",
                "front_class": "MBT_FRONT",
                "side_class": "MBT_SIDE",
                "rear_class": "MBT_REAR",
                "top_class": "MBT_TOP",
            },

            # -----------------------------------------------------
            # IFV
            # -----------------------------------------------------

            {
                "key": "BMP2_SARATH",
                "name": "Sarath",
                "designation": "BMP-2 Sarath",
                "platform_type": Platform.PlatformType.IFV,

                "manufacturer": "India",
                "country_of_origin": "India / Soviet origin",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_IFV",
                "amphibious": True,
                "night_capable": True,

                "description": (
                    "Indian BMP-2-derived infantry fighting vehicle. "
                    "Warpower India lists 2,500 units and describes "
                    "autocannon and missile-firing capability."
                ),

                "quantity": 2500,

                "protection_class": "IFV",
                "front_class": "IFV_FRONT",
                "side_class": "IFV_SIDE",
                "rear_class": "IFV_REAR",
                "top_class": "IFV_TOP",
            },

            # -----------------------------------------------------
            # ATGM CARRIER
            # -----------------------------------------------------

            {
                "key": "NAMICA",
                "name": "NAMICA",
                "designation": "NAg Missile Carrier",
                "platform_type": Platform.PlatformType.ATGM_CARRIER,

                "manufacturer": "India",
                "country_of_origin": "India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "TRACKED_ATGM",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Tracked anti-tank guided missile carrier "
                    "based on the BMP-2 family. Warpower India "
                    "lists 12 units and describes eight missiles "
                    "carried ready-to-fire."
                ),

                "quantity": 12,

                "protection_class": "IFV",
                "front_class": "IFV_FRONT",
                "side_class": "IFV_SIDE",
                "rear_class": "IFV_REAR",
                "top_class": "IFV_TOP",
            },

            # -----------------------------------------------------
            # APC
            # -----------------------------------------------------

            {
                "key": "KESTREL",
                "name": "Kestrel",
                "designation": "TATA Kestrel",
                "platform_type": Platform.PlatformType.APC,

                "manufacturer": "Tata",
                "country_of_origin": "India",

                "crew_size": 3,
                "passenger_capacity": 9,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": 26,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_8X8",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian 8x8 armoured personnel carrier. "
                    "Warpower India lists nine units, 26-tonne "
                    "weight, three crew and nine passengers."
                ),

                "quantity": 9,

                "protection_class": "APC",
                "front_class": "APC_FRONT",
                "side_class": "APC_SIDE",
                "rear_class": "APC_REAR",
                "top_class": "APC_TOP",
            },

            # -----------------------------------------------------
            # MRAP
            # -----------------------------------------------------

            {
                "key": "ADITYA",
                "name": "Aditya",
                "designation": "OFB Aditya",
                "platform_type": Platform.PlatformType.MRAP,

                "manufacturer": "India",
                "country_of_origin": "India",

                "crew_size": 2,
                "passenger_capacity": 10,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_4X4",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian infantry mobility vehicle / MRAP. "
                    "Warpower India lists 1,400 units and "
                    "describes a 4x4 configuration, two crew "
                    "and ten protected passengers."
                ),

                "quantity": 1400,

                "protection_class": "MRAP",
                "front_class": "MRAP_FRONT",
                "side_class": "MRAP_SIDE",
                "rear_class": "MRAP_REAR",
                "top_class": "MRAP_TOP",
            },

            {
                "key": "CASSPIR",
                "name": "Casspir",
                "designation": "Casspir",
                "platform_type": Platform.PlatformType.MRAP,

                "manufacturer": "",
                "country_of_origin": "South Africa",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_4X4",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "South African-origin MRAP used by India. "
                    "Warpower India lists around 200 units."
                ),

                "quantity": 200,

                "protection_class": "MRAP",
                "front_class": "MRAP_FRONT",
                "side_class": "MRAP_SIDE",
                "rear_class": "MRAP_REAR",
                "top_class": "MRAP_TOP",
            },

            {
                "key": "KALYANI_M4",
                "name": "Kalyani M4",
                "designation": "Kalyani M4",
                "platform_type": Platform.PlatformType.MRAP,

                "manufacturer": "Kalyani",
                "country_of_origin": "India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_4X4",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian protected mobility vehicle. "
                    "Warpower India lists 45 units."
                ),

                "quantity": 45,

                "protection_class": "MRAP",
                "front_class": "MRAP_FRONT",
                "side_class": "MRAP_SIDE",
                "rear_class": "MRAP_REAR",
                "top_class": "MRAP_TOP",
            },

            {
                "key": "QRFV",
                "name": "QRFV",
                "designation": "TATA QRFV",
                "platform_type": Platform.PlatformType.MRAP,

                "manufacturer": "Tata",
                "country_of_origin": "India",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_4X4",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Indian quick reaction fighting vehicle / MRAP. "
                    "Warpower India lists 36 units."
                ),

                "quantity": 36,

                "protection_class": "MRAP",
                "front_class": "MRAP_FRONT",
                "side_class": "MRAP_SIDE",
                "rear_class": "MRAP_REAR",
                "top_class": "MRAP_TOP",
            },

            # -----------------------------------------------------
            # LIGHT ARMOURED
            # -----------------------------------------------------

            {
                "key": "LMV",
                "name": "LMVs",
                "designation": "Light Armored Vehicles (Various)",
                "platform_type": Platform.PlatformType.LIGHT_ARMOURED,

                "manufacturer": "",
                "country_of_origin": "",

                "crew_size": None,
                "passenger_capacity": None,

                "length_m": None,
                "width_m": None,
                "height_m": None,
                "combat_weight_tonnes": None,

                "engine_power_kw": None,
                "max_speed_kmh": None,
                "operational_range_km": None,
                "fuel_capacity_litres": None,

                "mobility_class": "WHEELED_4X4",
                "amphibious": False,
                "night_capable": True,

                "description": (
                    "Aggregate light-armoured vehicle category. "
                    "Warpower India lists 2,200 units and describes "
                    "utility, scouting and security roles."
                ),

                "quantity": 2200,

                "protection_class": "LIGHT_ARMOURED",
                "front_class": "LIGHT_ARMOURED_FRONT",
                "side_class": "LIGHT_ARMOURED_SIDE",
                "rear_class": "LIGHT_ARMOURED_REAR",
                "top_class": "LIGHT_ARMOURED_TOP",
            },
        ]

        # =========================================================
        # 5. CREATE / UPDATE PLATFORMS
        # =========================================================

        platforms = {}

        for data in platforms_data:

            platform, created = Platform.objects.update_or_create(
                name=data["name"],
                defaults={
                    "designation": data["designation"],
                    "platform_type": data["platform_type"],

                    "manufacturer": data["manufacturer"],
                    "country_of_origin": data["country_of_origin"],

                    "crew_size": data["crew_size"],
                    "passenger_capacity": data["passenger_capacity"],

                    "length_m": data["length_m"],
                    "width_m": data["width_m"],
                    "height_m": data["height_m"],
                    "combat_weight_tonnes": (
                        data["combat_weight_tonnes"]
                    ),

                    "engine_power_kw": data["engine_power_kw"],
                    "max_speed_kmh": data["max_speed_kmh"],
                    "operational_range_km": (
                        data["operational_range_km"]
                    ),
                    "fuel_capacity_litres": (
                        data["fuel_capacity_litres"]
                    ),

                    "mobility_class": data["mobility_class"],
                    "amphibious": data["amphibious"],
                    "night_capable": data["night_capable"],

                    "description": data["description"],

                    "source": source,

                    "source_notes": (
                        "Inventory and descriptive characteristics "
                        "derived from the Warpower India Indian "
                        "Land Power reference page."
                    ),

                    "is_active": True,
                },
            )

            platforms[data["key"]] = platform

            # -----------------------------------------------------
            # FORCE INVENTORY
            # -----------------------------------------------------

            ForcePlatform.objects.update_or_create(
                force=indian_armoured,
                platform=platform,
                defaults={
                    "authorized_quantity": data["quantity"],
                    "is_available_for_scenario": True,
                },
            )

            # -----------------------------------------------------
            # ABSTRACT PROTECTION MODEL
            # -----------------------------------------------------

            PlatformProtection.objects.update_or_create(
                platform=platform,
                defaults={
                    "protection_class": data["protection_class"],
                    "front_class": data["front_class"],
                    "side_class": data["side_class"],
                    "rear_class": data["rear_class"],
                    "top_class": data["top_class"],
                    "notes": (
                        "Simulation protection classes only. "
                        "They are not measurements of actual armour "
                        "construction or classified protection."
                    ),
                    "source": source,
                },
            )

            action = "CREATED" if created else "UPDATED"

            self.stdout.write(
                f"[{action}] "
                f"{platform.name:<25} "
                f"{data['quantity']:>5} units"
            )

        # =========================================================
        # 6. WEAPONS
        # =========================================================

        weapons_data = [

            {
                "key": "T72_T90_MAIN_GUN",
                "name": "125mm MBT Main Gun",
                "designation": "125mm Smoothbore MBT Gun",
                "weapon_class": Weapon.WeaponClass.KINETIC,

                "caliber_mm": 125,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": True,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": True,

                "description": (
                    "Generic 125mm-class smoothbore MBT gun "
                    "category used for simulation."
                ),
            },

            {
                "key": "ARJUN_MAIN_GUN",
                "name": "120mm Arjun Main Gun",
                "designation": "120mm Rifled MBT Gun",
                "weapon_class": Weapon.WeaponClass.KINETIC,

                "caliber_mm": 120,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": True,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": True,

                "description": (
                    "Generic 120mm rifled MBT gun category "
                    "for the Arjun family."
                ),
            },

            {
                "key": "BMP2_30MM",
                "name": "30mm IFV Autocannon",
                "designation": "30mm Autocannon",
                "weapon_class": Weapon.WeaponClass.AUTOCANNON,

                "caliber_mm": 30,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": True,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": False,

                "description": (
                    "Generic 30mm IFV autocannon category."
                ),
            },

            {
                "key": "NAMICA_ATGM",
                "name": "NAMICA ATGM System",
                "designation": "NAg Missile System",
                "weapon_class": Weapon.WeaponClass.MISSILE,

                "caliber_mm": None,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": True,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": True,

                "description": (
                    "Generic NAMICA anti-tank guided missile "
                    "system category."
                ),
            },

            {
                "key": "KESTREL_30MM",
                "name": "Kestrel 30mm Cannon",
                "designation": "30mm Automatic Cannon",
                "weapon_class": Weapon.WeaponClass.AUTOCANNON,

                "caliber_mm": 30,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": True,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": False,

                "description": (
                    "30mm automatic cannon category for the "
                    "Kestrel platform."
                ),
            },

            {
                "key": "RWS_GENERIC",
                "name": "Remote Weapon Station",
                "designation": "Generic RWS",
                "weapon_class": Weapon.WeaponClass.MACHINE_GUN,

                "caliber_mm": None,
                "effective_range_m": None,
                "maximum_range_m": None,
                "rate_of_fire_rpm": None,
                "reload_time_seconds": None,

                "stabilized": False,
                "fire_control_system": "",
                "day_sight": True,
                "night_sight": True,
                "thermal_sight": False,

                "description": (
                    "Generic remote weapon station category "
                    "for protected vehicle simulation."
                ),
            },
        ]

        weapons = {}

        for data in weapons_data:

            weapon, _ = Weapon.objects.update_or_create(
                name=data["name"],
                defaults={
                    "designation": data["designation"],
                    "weapon_class": data["weapon_class"],

                    "caliber_mm": data["caliber_mm"],
                    "effective_range_m": data["effective_range_m"],
                    "maximum_range_m": data["maximum_range_m"],
                    "rate_of_fire_rpm": data["rate_of_fire_rpm"],
                    "reload_time_seconds": (
                        data["reload_time_seconds"]
                    ),

                    "stabilized": data["stabilized"],
                    "fire_control_system": (
                        data["fire_control_system"]
                    ),

                    "day_sight": data["day_sight"],
                    "night_sight": data["night_sight"],
                    "thermal_sight": data["thermal_sight"],

                    "description": data["description"],

                    "source": source,

                    "source_notes": (
                        "Weapon category created for the "
                        "simulation master dataset."
                    ),

                    "is_active": True,
                },
            )

            weapons[data["key"]] = weapon

        # =========================================================
        # 7. PLATFORM → WEAPON
        # =========================================================

        platform_weapons = [

            ("T72_AJEYA", "T72_T90_MAIN_GUN"),
            ("T90S_BHISHMA", "T72_T90_MAIN_GUN"),

            ("ARJUN_MK1", "ARJUN_MAIN_GUN"),
            ("ARJUN_MK1A", "ARJUN_MAIN_GUN"),

            ("BMP2_SARATH", "BMP2_30MM"),

            ("NAMICA", "NAMICA_ATGM"),

            ("KESTREL", "KESTREL_30MM"),

            ("ADITYA", "RWS_GENERIC"),
            ("CASSPIR", "RWS_GENERIC"),
            ("KALYANI_M4", "RWS_GENERIC"),
            ("QRFV", "RWS_GENERIC"),
            ("LMV", "RWS_GENERIC"),
        ]

        for platform_key, weapon_key in platform_weapons:

            PlatformWeapon.objects.update_or_create(
                platform=platforms[platform_key],
                weapon=weapons[weapon_key],
                defaults={
                    "quantity": 1,
                    "is_primary": True,
                },
            )

        # =========================================================
        # 8. AMMUNITION CATEGORIES
        # =========================================================

        ammunition_data = [

            {
                "key": "MBT_KINETIC",
                "name": "MBT Kinetic Training/Simulation Round",
                "designation": "Generic MBT Kinetic",
                "ammunition_type": Ammunition.AmmunitionType.KINETIC,
                "caliber_mm": 125,
                "description": (
                    "Abstract simulation ammunition category."
                ),
            },

            {
                "key": "MBT_CHEMICAL",
                "name": "MBT Chemical Energy Simulation Round",
                "designation": "Generic MBT Chemical Energy",
                "ammunition_type": Ammunition.AmmunitionType.CHEMICAL,
                "caliber_mm": 125,
                "description": (
                    "Abstract simulation ammunition category."
                ),
            },

            {
                "key": "IFV_30MM",
                "name": "30mm IFV Ammunition",
                "designation": "Generic 30mm",
                "ammunition_type": Ammunition.AmmunitionType.OTHER,
                "caliber_mm": 30,
                "description": (
                    "Abstract 30mm simulation ammunition category."
                ),
            },

            {
                "key": "ATGM_GENERIC",
                "name": "ATGM Simulation Missile",
                "designation": "Generic ATGM",
                "ammunition_type": Ammunition.AmmunitionType.ATGM,
                "caliber_mm": None,
                "description": (
                    "Abstract anti-tank guided missile "
                    "simulation category."
                ),
            },
        ]

        ammunition = {}

        for data in ammunition_data:

            item, _ = Ammunition.objects.update_or_create(
                name=data["name"],
                defaults={
                    "designation": data["designation"],
                    "ammunition_type": data["ammunition_type"],
                    "caliber_mm": data["caliber_mm"],
                    "description": data["description"],
                    "source": source,
                    "source_notes": (
                        "Abstract simulation ammunition category; "
                        "not a representation of classified "
                        "or restricted ammunition data."
                    ),
                    "is_active": True,
                },
            )

            ammunition[data["key"]] = item

        # =========================================================
        # 9. WEAPON → AMMUNITION
        # =========================================================

        weapon_ammunition = [

            ("T72_T90_MAIN_GUN", "MBT_KINETIC"),
            ("T72_T90_MAIN_GUN", "MBT_CHEMICAL"),

            ("ARJUN_MAIN_GUN", "MBT_KINETIC"),
            ("ARJUN_MAIN_GUN", "MBT_CHEMICAL"),

            ("BMP2_30MM", "IFV_30MM"),
            ("KESTREL_30MM", "IFV_30MM"),

            ("NAMICA_ATGM", "ATGM_GENERIC"),
        ]

        for weapon_key, ammo_key in weapon_ammunition:

            WeaponAmmunition.objects.update_or_create(
                weapon=weapons[weapon_key],
                ammunition=ammunition[ammo_key],
                defaults={
                    "authorized_quantity": 0,
                    "is_primary": True,
                },
            )

        # =========================================================
        # 10. BASIC SENSOR CATEGORIES
        # =========================================================

        sensors_data = [

            {
                "key": "OPTICAL_DAY",
                "name": "Day Optical Sight",
                "sensor_type": Sensor.SensorType.OPTICAL,
                "description": (
                    "Generic day optical sensor category."
                ),
            },

            {
                "key": "THERMAL",
                "name": "Thermal Imaging Sensor",
                "sensor_type": Sensor.SensorType.THERMAL,
                "description": (
                    "Generic thermal imaging sensor category."
                ),
            },

            {
                "key": "LASER_RANGEFINDER",
                "name": "Laser Rangefinder",
                "sensor_type": Sensor.SensorType.LASER,
                "description": (
                    "Generic laser rangefinder category."
                ),
            },
        ]

        sensors = {}

        for data in sensors_data:

            sensor, _ = Sensor.objects.update_or_create(
                name=data["name"],
                defaults={
                    "sensor_type": data["sensor_type"],
                    "detection_range_m": None,
                    "identification_range_m": None,
                    "night_capable": (
                        data["key"] != "OPTICAL_DAY"
                    ),
                    "weather_degradation": True,
                    "description": data["description"],
                    "source": source,
                },
            )

            sensors[data["key"]] = sensor

        # =========================================================
        # 11. PLATFORM → SENSOR
        #
        # These are generic capability categories, not exact
        # sensor fitment claims.
        # =========================================================

        platform_sensors = [

            ("T72_AJEYA", "OPTICAL_DAY"),
            ("T72_AJEYA", "LASER_RANGEFINDER"),

            ("T90S_BHISHMA", "OPTICAL_DAY"),
            ("T90S_BHISHMA", "THERMAL"),
            ("T90S_BHISHMA", "LASER_RANGEFINDER"),

            ("ARJUN_MK1", "OPTICAL_DAY"),
            ("ARJUN_MK1", "THERMAL"),
            ("ARJUN_MK1", "LASER_RANGEFINDER"),

            ("ARJUN_MK1A", "OPTICAL_DAY"),
            ("ARJUN_MK1A", "THERMAL"),
            ("ARJUN_MK1A", "LASER_RANGEFINDER"),

            ("BMP2_SARATH", "OPTICAL_DAY"),
            ("NAMICA", "OPTICAL_DAY"),
            ("KESTREL", "OPTICAL_DAY"),
        ]

        for platform_key, sensor_key in platform_sensors:

            PlatformSensor.objects.update_or_create(
                platform=platforms[platform_key],
                sensor=sensors[sensor_key],
                defaults={
                    "quantity": 1,
                    "is_primary": True,
                },
            )

        # =========================================================
        # 12. SUMMARY
        # =========================================================

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "  SEED COMPLETED SUCCESSFULLY"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                "=============================================="
            )
        )

        self.stdout.write("")
        self.stdout.write(
            f"Platforms: {len(platforms_data)}"
        )

        self.stdout.write(
            "MBTs: 4"
        )

        self.stdout.write(
            "IFVs: 1"
        )

        self.stdout.write(
            "ATGM carriers: 1"
        )

        self.stdout.write(
            "APCs: 1"
        )

        self.stdout.write(
            "MRAPs: 4"
        )

        self.stdout.write(
            "Light armoured category: 1"
        )

        self.stdout.write("")
        self.stdout.write(
            f"Source: {self.SOURCE_URL}"
        )