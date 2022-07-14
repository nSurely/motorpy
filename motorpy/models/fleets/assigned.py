import motorpy.models as models
from pydantic import Field
from typing import Optional, Tuple
from datetime import datetime


class FleetDriverVehicleAssignment(models.PrivateAPIHandler):
    "FDRV Assignment. This represents a vehicle that a driver is assigned to."
    expires_at: Optional[datetime] = Field(
        default=None,
        alias="expiresAt"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt"
    )
    is_active: bool = Field(
        default=False,
        alias="isActive"
    )
    is_assigned: bool = Field(
        default=False,
        alias="assigned"
    )
    source_id: Optional[str] = Field(
        default=None,
        alias="sourceId"
    )

    vehicle: Optional['models.Vehicle'] = Field(
        default=None,
        alias="registeredVehicle"
    )

    driver: Optional['models.Driver'] = Field(
        default=None,
        alias="driver"
    )

    @property
    def id(self) -> Tuple[Optional[str], Optional[str]]:
        "Returns the driver and vehicle ID if the vehicle is set"
        return self.driver.id if self.driver else None, self.vehicle.id if self.vehicle else None
    
    @property
    def telematics_id(self) -> str:
        """
        Return the telematics ID.

        Returns:
            str: telematics ID
        """
        return self.source_id
