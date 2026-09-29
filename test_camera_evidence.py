import cv2

from src.camera.road_analyzer import RoadAnalyzer
from src.camera.camera_evidence import CameraEvidenceAnalyzer


image = cv2.imread("camera_test_input.jpg")

if image is None:
    raise FileNotFoundError(
        "camera_test_input.jpg not found"
    )


road_analyzer = RoadAnalyzer()
evidence_analyzer = CameraEvidenceAnalyzer()


road_result = road_analyzer.analyze(image)


evidence = evidence_analyzer.analyze(
    edge_density=road_result["edge_density"],
    brightness=road_result["brightness"],
)


print("Camera evidence analysis:")

print(
    "Edge density:",
    round(evidence.edge_density, 4),
)

print(
    "Brightness:",
    round(evidence.brightness, 4),
)

print(
    "Hazard evidence score:",
    round(evidence.hazard_score, 4),
)

print(
    "Confidence:",
    round(evidence.confidence, 4),
)