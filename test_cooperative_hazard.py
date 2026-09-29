from src.events.event_factory import create_traction_event
from src.hazards.hazard_aggregator import HazardAggregator
from src.hazards.warning_manager import WarningManager


# The road location we are monitoring
ROAD_LATITUDE = 52.5201
ROAD_LONGITUDE = 13.4052


def create_vehicle_event(
    vehicle_id: str,
    intensity: float,
    duration: float,
):
    """Create a simulated traction event near the same road location."""

    return create_traction_event(
        vehicle_id=vehicle_id,
        latitude=ROAD_LATITUDE,
        longitude=ROAD_LONGITUDE,
        vehicle_speed_kmh=50.0,
        intensity=intensity,
        duration_seconds=duration,
    )


# --------------------------------------------------
# Create cooperative hazard aggregator
# --------------------------------------------------

aggregator = HazardAggregator()

warning_manager = WarningManager()


# --------------------------------------------------
# Vehicle 1
# --------------------------------------------------

event_1 = create_vehicle_event(
    vehicle_id="V001",
    intensity=0.40,
    duration=1.2,
)

aggregator.add_event(event_1)

score_1 = aggregator.calculate_score(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

state_1 = aggregator.get_state(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

update_1 = warning_manager.update(state_1)

print("=== AFTER VEHICLE 1 ===")
print("Score:", round(score_1, 2))
print("State:", state_1)
print("Beep:", update_1.beep)


# --------------------------------------------------
# Vehicle 2
# --------------------------------------------------

event_2 = create_vehicle_event(
    vehicle_id="V002",
    intensity=0.65,
    duration=1.8,
)

aggregator.add_event(event_2)

score_2 = aggregator.calculate_score(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

state_2 = aggregator.get_state(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

update_2 = warning_manager.update(state_2)

print("\n=== AFTER VEHICLE 2 ===")
print("Score:", round(score_2, 2))
print("State:", state_2)
print("Beep:", update_2.beep)


# --------------------------------------------------
# Vehicle 3
# --------------------------------------------------

event_3 = create_vehicle_event(
    vehicle_id="V003",
    intensity=0.75,
    duration=2.0,
)

aggregator.add_event(event_3)

score_3 = aggregator.calculate_score(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

state_3 = aggregator.get_state(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

update_3 = warning_manager.update(state_3)

print("\n=== AFTER VEHICLE 3 ===")
print("Score:", round(score_3, 2))
print("State:", state_3)
print("Beep:", update_3.beep)


# --------------------------------------------------
# Vehicle 4
# --------------------------------------------------

event_4 = create_vehicle_event(
    vehicle_id="V004",
    intensity=0.90,
    duration=2.5,
)

aggregator.add_event(event_4)

score_4 = aggregator.calculate_score(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

state_4 = aggregator.get_state(
    ROAD_LATITUDE,
    ROAD_LONGITUDE,
)

update_4 = warning_manager.update(state_4)

print("\n=== AFTER VEHICLE 4 ===")
print("Score:", round(score_4, 2))
print("State:", state_4)
print("Beep:", update_4.beep)


print("\n=== COOPERATIVE HAZARD COMPLETE ===")