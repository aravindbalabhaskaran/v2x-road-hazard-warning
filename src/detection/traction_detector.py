from statistics import mean


class TractionDetector:
    """Detects potential traction loss from wheel-speed differences."""

    def __init__(self, slip_threshold: float = 0.15):
        self.slip_threshold = slip_threshold

    def detect(
        self,
        vehicle_speed_kmh: float,
        wheel_speeds_kmh: list[float],
    ) -> tuple[bool, float]:
        """
        Detect potential traction loss.

        Returns:
            detected: True if traction loss is suspected.
            intensity: Estimated traction-loss intensity from 0 to 1.
        """

        if vehicle_speed_kmh <= 0:
            return False, 0.0

        average_wheel_speed = mean(wheel_speeds_kmh)

        slip_ratio = abs(
            average_wheel_speed - vehicle_speed_kmh
        ) / vehicle_speed_kmh

        if slip_ratio <= self.slip_threshold:
            return False, 0.0

        intensity = min(
            slip_ratio / 0.50,
            1.0,
        )

        return True, intensity