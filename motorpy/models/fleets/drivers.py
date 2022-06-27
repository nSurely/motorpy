from pydantic import Field
from typing import Optional
from motorpy.models import PrivateAPIHandler
from motorpy.models.drivers import Driver
from datetime import datetime


class FleetDriver(PrivateAPIHandler):
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

    driver: Optional[Driver] = Field(
        default=None,
        alias="driver"
    )

    @property
    def id(self) -> Optional[str]:
        return self.driver.id if self.driver else None
    
    @property
    def full_name(self) -> Optional[str]:
        return self.driver.full_name if self.driver else None