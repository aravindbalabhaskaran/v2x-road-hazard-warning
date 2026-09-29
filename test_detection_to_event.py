from src.detection.traction_detector import TractionDetector
from src.events.event_factory import create_traction_event


detector = TractionDetector()


# Simulated vehicle sensor data
vehicle_speed = 50.0
wheel_speeds = [68.0, 66.0, 51.0, 52.0]


# Detect traction loss
detected, intensity = detector.detect(
    vehicle_speed_kmh=vehicle_speed,
    wheel_speeds_kmh=wheel_speeds,
)


if detected:
    event = create_traction_event(
        vehicle_id="V001",
        latitude=52.5201,
        longitude=13.4052,
        vehicle_speed_kmh=vehicle_speed,
        intensity=intensity,
        duration_seconds=1.5,
    )

    print("Traction event detected!")
    print(event)

else:
    print("No traction event detected.")