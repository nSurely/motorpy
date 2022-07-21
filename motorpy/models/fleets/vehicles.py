import motorpy.models as models
from pydantic import Field
from typing import Optional
from datetime import datetime


class FleetVehicle(models.PrivateAPIHandler):
    "Represents a vehicle that is assigned to a fleet"
    source_id: Optional[str] = Field(
        default=None,
        alias="sourceId"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        alias="expiresAt"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt"
    )

    vehicle: Optional['models.Vehicle'] = Field(
        default=None,
        alias="registeredVehicle"
    )

    @property
    def id(self) -> Optional[str]:
        "Returns the vehicle ID if the vehicle is set"
        return self.vehicle.id if self.vehicle else None
