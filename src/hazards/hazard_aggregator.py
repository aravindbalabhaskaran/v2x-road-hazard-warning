from datetime import datetime, timezone
from math import radians, sin, cos, sqrt, atan2

from src.events.hazard_event import TractionEvent


class HazardAggregator:
    """Aggregates recent nearby traction events into a road-hazard state."""

    def __init__(
        self,
        correlation_radius_m: float = 100.0,
        max_event_age_seconds: float = 300.0,
    ):
        self.events: list[TractionEvent] = []
        self.correlation_radius_m = correlation_radius_m
        self.max_event_age_seconds = max_event_age_seconds

    def add_event(self, event: TractionEvent) -> None:
        """Add a vehicle-reported traction event."""
        self.events.append(event)

    def _distance_m(
        self,
        latitude_1: float,
        longitude_1: float,
        latitude_2: float,
        longitude_2: float,
    ) -> float:
        """Calculate approximate distance between two GPS coordinates."""

        earth_radius_m = 6_371_000

        lat1 = radians(latitude_1)
        lat2 = radians(latitude_2)

        delta_lat = radians(latitude_2 - latitude_1)
        delta_lon = radians(longitude_2 - longitude_1)

        a = (
            sin(delta_lat / 2) ** 2
            + cos(lat1)
            * cos(lat2)
            * sin(delta_lon / 2) ** 2
        )

        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return earth_radius_m * c

    def _event_age_seconds(
        self,
        event: TractionEvent,
    ) -> float:
        """Return the age of an event in seconds."""

        now = datetime.now(timezone.utc)

        return max(
            0.0,
            (now - event.timestamp).total_seconds(),
        )

    def _recent_events(self) -> list[TractionEvent]:
        """Return events that are still considered fresh."""

        return [
            event
            for event in self.events
            if self._event_age_seconds(event)
            <= self.max_event_age_seconds
        ]

    def _nearby_events(
        self,
        latitude: float,
        longitude: float,
    ) -> list[TractionEvent]:
        """Return recent events within the correlation radius."""

        recent_events = self._recent_events()

        return [
            event
            for event in recent_events
            if self._distance_m(
                latitude,
                longitude,
                event.latitude,
                event.longitude,
            ) <= self.correlation_radius_m
        ]

    def _time_weight(
        self,
        event: TractionEvent,
    ) -> float:
        """Calculate a linear freshness weight from 1 to 0."""

        age = self._event_age_seconds(event)

        if age >= self.max_event_age_seconds:
            return 0.0

        return 1.0 - (
            age / self.max_event_age_seconds
        )

    def _duration_weight(
        self,
        event: TractionEvent,
    ) -> float:
        """Convert event duration into a normalized weight."""

        return min(
            event.duration_seconds / 3.0,
            1.0,
        )

    def calculate_score(
        self,
        latitude: float,
        longitude: float,
    ) -> float:
        """Calculate hazard score using recent nearby events."""

        nearby_events = self._nearby_events(
            latitude,
            longitude,
        )

        if not nearby_events:
            return 0.0

        weighted_evidence = 0.0

        for event in nearby_events:
            time_weight = self._time_weight(event)
            duration_weight = self._duration_weight(event)

            event_evidence = (
                event.intensity
                * time_weight
                * (0.5 + 0.5 * duration_weight)
            )

            weighted_evidence += event_evidence

        event_score = min(
            len(nearby_events) / 5,
            1.0,
        ) * 50

        evidence_score = min(
            weighted_evidence / 3,
            1.0,
        ) * 50

        score = event_score + evidence_score

        return min(score, 100.0)

    def get_state(
        self,
        latitude: float,
        longitude: float,
    ) -> str:
        """Convert the local hazard score into a warning state."""

        score = self.calculate_score(
            latitude,
            longitude,
        )

        if score < 30:
            return "WHITE"

        if score < 65:
            return "YELLOW"

        return "RED"