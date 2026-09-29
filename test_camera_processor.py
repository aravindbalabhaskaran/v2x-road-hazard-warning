import cv2
import numpy as np

from src.camera.camera_processor import CameraProcessor


processor = CameraProcessor()


# Create a synthetic road-like test image.
image = np.zeros(
    (720, 1280, 3),
    dtype=np.uint8,
)

# Road area
cv2.rectangle(
    image,
    (0, 300),
    (1280, 720),
    (120, 120, 120),
    -1,
)

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


# Save original camera image
cv2.imwrite(
    "camera_test_input.jpg",
    image,
)


# Process the image
resized = processor.resize_image(image)
enhanced = processor.enhance_image(resized)


# Save processed image
cv2.imwrite(
    "camera_test_output.jpg",
    enhanced,
)


print("Camera processing test successful!")
print("Original shape:", image.shape)
print("Processed shape:", enhanced.shape)
print("Saved original: camera_test_input.jpg")
print("Saved processed: camera_test_output.jpg")