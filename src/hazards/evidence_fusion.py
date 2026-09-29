from dataclasses import dataclass


@dataclass
class FusionResult:
    """Combined vehicle and camera hazard evidence."""

    vehicle_score: float
    camera_score: float
    combined_score: float
    confidence: float


class EvidenceFusion:
    """Combines vehicle-dynamics and camera evidence."""

    def __init__(
        self,
        vehicle_weight: float = 0.65,
        camera_weight: float = 0.35,
    ):
        self.vehicle_weight = vehicle_weight
        self.camera_weight = camera_weight

    def combine(
        self,
        vehicle_score: float,
        camera_score: float,
    ) -> FusionResult:
        """
        Combine vehicle and camera evidence.

        Scores are normalized between 0 and 1.
        """

        vehicle_score = max(
            0.0,
            min(vehicle_score, 1.0),
        )

        camera_score = max(
            0.0,
            min(camera_score, 1.0),
        )

        combined_score = (
            vehicle_score * self.vehicle_weight
            + camera_score * self.camera_weight
        )

        # When both sources provide evidence,
        # confidence increases because the observations
        # support each other.
        agreement = min(
            vehicle_score,
            camera_score,
        )

        confidence = min(
            0.5
            + combined_score * 0.35
            + agreement * 0.15,
            1.0,
        )

        return FusionResult(
            vehicle_score=vehicle_score,
            camera_score=camera_score,
            combined_score=combined_score,
            confidence=confidence,
        )