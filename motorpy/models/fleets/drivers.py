import motorpy.models as models
from pydantic import Field
from typing import Optional
from datetime import datetime


class FleetDriver(models.PrivateAPIHandler):
    "Represents a driver who is assigned to a fleet"
    # fleet id is returned on the driver record
    fleet_id: Optional[str] = Field(
        default=None,
        alias="id"
    )
    # fd source id
    source_id: Optional[str] = Field(
        default=None,
        alias="sourceId"
    )
    is_vehicle_manager: bool = Field(
        default=False,
        alias="isVehicleManager"
    )
    is_driver_manager: bool = Field(
        default=False,
        alias="isDriverManager"
    )
    is_billing_manager: bool = Field(
        default=False,
        alias="isBillingManager"
    )
    is_active: bool = Field(
        default=False,
        alias="isActive"
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        alias="expiresAt"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt"
    )

    driver: Optional['models.Driver'] = Field(
        default=None,
        alias="driver"
    )

    @property
    def id(self) -> Optional[str]:
        "Returns the driver ID if the driver is set"
        return self.driver.id if self.driver else None

    @property
    def full_name(self) -> Optional[str]:
        "Returns the driver full name if the driver is set"
        return self.driver.full_name if self.driver else None

    @property
    def telematics_id(self) -> str:
        """
        Return the telematics ID.

        Returns:
            str: telematics ID
        """
        return self.source_id

    async def get_fleet(self) -> Optional['models.Fleet']:
        """
        Return the fleet.

        Returns:
            models.Fleet: fleet
        """
        return models.Fleet(api=self.api, **(await self.api.request("GET", f"fleets/{self.fleet_id}"))) if self.fleet_id else None
