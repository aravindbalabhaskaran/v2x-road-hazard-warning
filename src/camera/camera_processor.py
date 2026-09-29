import cv2
import numpy as np


class CameraProcessor:
    """Basic camera-image processing for road-condition analysis."""

    def __init__(self):
        pass

    def load_image(self, image_path: str) -> np.ndarray:
        """Load an image from disk."""

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Could not load image: {image_path}"
            )

        return image

    def resize_image(
        self,
        image: np.ndarray,
        width: int = 1280,
    ) -> np.ndarray:
        """Resize image while maintaining aspect ratio."""

        height, original_width = image.shape[:2]

        if original_width <= width:
            return image

        scale = width / original_width
        new_height = int(height * scale)

        return cv2.resize(
            image,
            (width, new_height),
        )

    def enhance_image(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """Apply basic image enhancement."""

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        denoised = cv2.GaussianBlur(
            gray,
            (5, 5),
            0,
        )

        enhanced = cv2.equalizeHist(
            denoised,
        )

        return enhanced