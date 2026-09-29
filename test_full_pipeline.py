from src.detection.traction_detector import TractionDetector
from src.events.event_factory import create_traction_event
from src.hazards.hazard_aggregator import HazardAggregator
from src.hazards.evidence_fusion import EvidenceFusion
from src.hazards.warning_manager import WarningManager
from src.camera.road_analyzer import RoadAnalyzer
from src.camera.camera_evidence import CameraEvidenceAnalyzer

import cv2


# --------------------------------------------------
# 1. VEHICLE DYNAMICS
# --------------------------------------------------

detector = TractionDetector()

detected, intensity = detector.detect(
    vehicle_speed_kmh=50.0,
    wheel_speeds_kmh=[
        68.0,
        66.0,
        51.0,
        52.0,
    ],
)

print("=== VEHICLE DYNAMICS ===")
print("Traction detected:", detected)
print("Intensity:", round(intensity, 3))


# --------------------------------------------------
# 2. CREATE TRACTION EVENT
# --------------------------------------------------

event = create_traction_event(
    vehicle_id="V001",
    latitude=52.5201,
    longitude=13.4052,
    vehicle_speed_kmh=50.0,
    intensity=intensity,
    duration_seconds=1.5,
)

print("\n=== TRACTION EVENT ===")
print(event)


# --------------------------------------------------
# 3. HAZARD AGGREGATION
# --------------------------------------------------

aggregator = HazardAggregator()

aggregator.add_event(event)

vehicle_hazard_score = aggregator.calculate_score(
    latitude=52.5201,
    longitude=13.4052,
)

vehicle_score_normalized = (
    vehicle_hazard_score / 100.0
)

print("\n=== VEHICLE HAZARD ===")
print(
    "Vehicle hazard score:",
    round(vehicle_hazard_score, 2),
)

print(
    "Normalized vehicle score:",
    round(vehicle_score_normalized, 3),
)


# --------------------------------------------------
# 4. CAMERA ANALYSIS
# --------------------------------------------------

image = cv2.imread(
    "camera_test_input.jpg"
)

if image is None:
    raise FileNotFoundError(
        "camera_test_input.jpg not found"
    )


road_analyzer = RoadAnalyzer()

camera_features = road_analyzer.analyze(
    image
)

camera_evidence_analyzer = (
    CameraEvidenceAnalyzer()
)

camera_evidence = (
    camera_evidence_analyzer.analyze(
        edge_density=camera_features[
            "edge_density"
        ],
        brightness=camera_features[
            "brightness"
        ],
    )
)

print("\n=== CAMERA EVIDENCE ===")

print(
    "Camera hazard score:",
    round(
        camera_evidence.hazard_score,
        3,
    ),
)

print(
    "Camera confidence:",
    round(
        camera_evidence.confidence,
        3,
    ),
)


# --------------------------------------------------
# 5. EVIDENCE FUSION
# --------------------------------------------------

fusion = EvidenceFusion()

fusion_result = fusion.combine(
    vehicle_score=vehicle_score_normalized,
    camera_score=camera_evidence.hazard_score,
)

print("\n=== EVIDENCE FUSION ===")

print(
    "Combined score:",
    round(
        fusion_result.combined_score,
        3,
    ),
)

print(
    "Combined confidence:",
    round(
        fusion_result.confidence,
        3,
    ),
)


# --------------------------------------------------
# 6. CONVERT COMBINED SCORE TO WARNING STATE
# --------------------------------------------------

combined_score_100 = (
    fusion_result.combined_score * 100
)

if combined_score_100 < 30:
    warning_state = "WHITE"

elif combined_score_100 < 65:
    warning_state = "YELLOW"

else:
    warning_state = "RED"


print("\n=== WARNING STATE ===")

print(
    "Combined score:",
    round(
        combined_score_100,
        2,
    ),
)

print(
    "Warning state:",
    warning_state,
)


# --------------------------------------------------
# 7. WARNING MANAGER
# --------------------------------------------------

warning_manager = WarningManager()

warning_update = warning_manager.update(
    warning_state
)

print("\n=== DRIVER WARNING ===")

print(
    "Previous state:",
    warning_update.previous_state,
)

print(
    "Current state:",
    warning_update.current_state,
)

print(
    "Beep:",
    warning_update.beep,
)


print("\n=== PIPELINE COMPLETE ===")