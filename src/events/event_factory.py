from datetime import datetime, timezone
from uuid import uuid4

from src.events.hazard_event import TractionEvent


def create_traction_event(
    vehicle_id: str,
    latitude: float,
    longitude: float,
    vehicle_speed_kmh: float,
    intensity: float,
    duration_seconds: float,
) -> TractionEvent:
    """Create a structured traction event."""

    return TractionEvent(
        event_id=str(uuid4()),
        vehicle_id=vehicle_id,
        timestamp=datetime.now(timezone.utc),
        latitude=latitude,
        longitude=longitude,
        vehicle_speed_kmh=vehicle_speed_kmh,
        intensity=intensity,
        duration_seconds=duration_seconds,
    )