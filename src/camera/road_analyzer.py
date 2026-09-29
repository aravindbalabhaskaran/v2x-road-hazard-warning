import cv2
import numpy as np


class RoadAnalyzer:
    """Extracts and analyzes the road region of a camera image."""

    def __init__(self):
        pass

    def extract_road_region(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """Extract the lower portion of the image where the road is expected."""

        height, width = image.shape[:2]

        start_y = int(height * 0.45)

        road_region = image[
            start_y:height,
            0:width,
        ]

        return road_region

    def calculate_edge_density(
        self,
        road_region: np.ndarray,
    ) -> float:
        """Calculate normalized edge density in the road region."""

        gray = cv2.cvtColor(
            road_region,
            cv2.COLOR_BGR2GRAY,
        )

        edges = cv2.Canny(
            gray,
            50,
            150,
        )

        edge_pixels = np.count_nonzero(edges)
        total_pixels = edges.size

        return edge_pixels / total_pixels

    def calculate_brightness(
        self,
        road_region: np.ndarray,
    ) -> float:
        """Calculate normalized average brightness."""

        gray = cv2.cvtColor(
            road_region,
            cv2.COLOR_BGR2GRAY,
        )

        brightness = float(np.mean(gray))

        return brightness / 255.0

    def analyze(
        self,
        image: np.ndarray,
    ) -> dict:
        """Analyze the visible road region."""

        road_region = self.extract_road_region(
            image
        )

        edge_density = self.calculate_edge_density(
            road_region
        )

        brightness = self.calculate_brightness(
            road_region
        )

        return {
            "edge_density": edge_density,
            "brightness": brightness,
            "road_region_height": road_region.shape[0],
            "road_region_width": road_region.shape[1],
        }