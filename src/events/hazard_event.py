from datetime import datetime

from pydantic import BaseModel, Field


class TractionEvent(BaseModel):
    """Represents a vehicle-reported traction event."""

    event_id: str
    vehicle_id: str
    timestamp: datetime

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)

    vehicle_speed_kmh: float = Field(ge=0)
    intensity: float = Field(ge=0, le=1)
    duration_seconds: float = Field(gt=0)