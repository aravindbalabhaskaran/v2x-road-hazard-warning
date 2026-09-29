import cv2
import numpy as np

from src.camera.road_analyzer import RoadAnalyzer


analyzer = RoadAnalyzer()


# Create a synthetic road image.
image = np.zeros(
    (720, 1280, 3),
    dtype=np.uint8,
)

# Sky/background
image[:300] = (180, 180, 180)

# Road
image[300:] = (100, 100, 100)

# Lane markings
cv2.line(
    image,
    (400, 720),
    (600, 300),
    (255, 255, 255),
    8,
)

cv2.line(
    image,
    (880, 720),
    (680, 300),
    (255, 255, 255),
    8,
)


result = analyzer.analyze(image)


print("Road analysis successful!")
print("Edge density:", round(result["edge_density"], 4))
print("Brightness:", round(result["brightness"], 4))
print(
    "Road region:",
    result["road_region_width"],
    "x",
    result["road_region_height"],
)