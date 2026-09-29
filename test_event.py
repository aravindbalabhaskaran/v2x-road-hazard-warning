from datetime import datetime, timezone

from src.events.hazard_event import TractionEvent


event = TractionEvent(
    event_id="E0001",
    vehicle_id="V001",
    timestamp=datetime.now(timezone.utc),
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=48.0,
    intensity=0.72,
    duration_seconds=1.4,
)

print("Traction event created successfully!")
print(event)