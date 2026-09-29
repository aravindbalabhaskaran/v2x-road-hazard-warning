from src.detection.traction_detector import TractionDetector


detector = TractionDetector()


# Normal driving
normal_detected, normal_intensity = detector.detect(
    vehicle_speed_kmh=50.0,
    wheel_speeds_kmh=[50.2, 50.1, 50.3, 50.2],
)

print("Normal driving:")
print("Detected:", normal_detected)
print("Intensity:", normal_intensity)


# Simulated traction loss
traction_detected, traction_intensity = detector.detect(
    vehicle_speed_kmh=50.0,
    wheel_speeds_kmh=[68.0, 66.0, 51.0, 52.0],
)

print("\nTraction-loss scenario:")
print("Detected:", traction_detected)
print("Intensity:", traction_intensity)