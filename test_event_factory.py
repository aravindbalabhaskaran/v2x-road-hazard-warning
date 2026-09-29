from src.events.event_factory import create_traction_event


event = create_traction_event(
    vehicle_id="V001",
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=50.0,
    intensity=0.37,
    duration_seconds=1.5,
)

print("Event created successfully!")
print(event)