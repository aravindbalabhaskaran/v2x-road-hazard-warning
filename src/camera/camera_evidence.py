from dataclasses import dataclass


@dataclass
class CameraEvidence:
    """Represents visual evidence extracted from the road image."""

    hazard_score: float
    edge_density: float
    brightness: float
    confidence: float


class CameraEvidenceAnalyzer:
    """Converts road-image features into prototype hazard evidence."""

    def analyze(
        self,
        edge_density: float,
        brightness: float,
    ) -> CameraEvidence:

        # Prototype heuristic only.
        # These values are experimental and are NOT safety thresholds.

        texture_score = min(
            edge_density / 0.05,
            1.0,
        )

        brightness_score = 1.0 - abs(
            brightness - 0.45
        ) / 0.45

        brightness_score = max(
            0.0,
            min(brightness_score, 1.0),
        )

        hazard_score = (
            texture_score * 0.6
            + brightness_score * 0.4
        )

        confidence = min(
            0.5 + hazard_score * 0.5,
            1.0,
        )

        return CameraEvidence(
            hazard_score=hazard_score,
            edge_density=edge_density,
            brightness=brightness,
            confidence=confidence,
        )