from datetime import datetime, timedelta, timezone

from src.events.event_factory import create_traction_event
from src.events.hazard_event import TractionEvent
from src.hazards.hazard_aggregator import HazardAggregator


aggregator = HazardAggregator()


# Vehicle 1 reports a recent traction event
event_1 = create_traction_event(
    vehicle_id="V001",
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=50.0,
    intensity=0.37,
    duration_seconds=1.5,
)

aggregator.add_event(event_1)


# Vehicle 2 reports a recent nearby traction event
event_2 = create_traction_event(
    vehicle_id="V002",
    latitude=52.5202,
    longitude=13.4053,
    vehicle_speed_kmh=48.0,
    intensity=0.65,
    duration_seconds=2.0,
)

aggregator.add_event(event_2)


# Vehicle 3 reports another recent nearby event
event_3 = create_traction_event(
    vehicle_id="V003",
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=46.0,
    intensity=0.80,
    duration_seconds=2.5,
)

aggregator.add_event(event_3)


# Vehicle 4 reports a strong event far away
event_4 = create_traction_event(
    vehicle_id="V004",
    latitude=52.5300,
    longitude=13.4200,
    vehicle_speed_kmh=45.0,
    intensity=1.00,
    duration_seconds=3.0,
)

aggregator.add_event(event_4)


# Vehicle 5 reports a strong event nearby, but 10 minutes ago
old_timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)

event_5 = TractionEvent(
    event_id="OLD001",
    vehicle_id="V005",
    timestamp=old_timestamp,
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=45.0,
    intensity=1.00,
    duration_seconds=3.0,
)

aggregator.add_event(event_5)


# Check hazard at the location of Vehicle 1
check_latitude = 52.5201
check_longitude = 13.4052

score = aggregator.calculate_score(
    latitude=check_latitude,
    longitude=check_longitude,
)

state = aggregator.get_state(
    latitude=check_latitude,
    longitude=check_longitude,
)


print("Hazard check:")
print("Score:", round(score, 2))
print("State:", state)