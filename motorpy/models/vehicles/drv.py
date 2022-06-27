from pydantic import Field
from typing import Optional
from motorpy.models import PrivateAPIHandler
from datetime import datetime
from motorpy.models.risk import CommonRisk
from .rv import Vehicle


class DriverVehicle(PrivateAPIHandler, CommonRisk):
    id: str = Field(
        default=...,
        alias="id",
        title="RV ID",
        description="The unique ID of this registered vehicle."
    )
    source_id: str = Field(
        default=None,
        alias="sourceId",
        title="Source ID (telematics)",
        description="""The source ID (telematics tracking ID).  
        This source ID type is often used in fleet management.  
        Any billing events tied to this ID will be charged back to a driver through a DRV, or to the attached fleet.  
        
        > Contact nSurely to see what source ID is best for your use-case."""
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt",
        title="Created At",
        description="When this RV was added to the system."
    )

    display_name: Optional[str] = Field(
        default=None,
        alias="displayName",
        title="Display Name",
        description="Text field uploaded by the driver to quickly identify the DRV during selection."
    )
    is_approved: bool = Field(
        default=False,
        alias="isApproved",
        title="Is Approved",
        description="If this vehicle has been approved to be insured internally."
    )
    approved_at: Optional[datetime] = Field(
        default=None,
        alias="approvedAt",
        title="Approved At",
        description="The ISO timestamp of when this vehicle was approved internally."
    )
    is_owner: bool = Field(
        default=False,
        alias="isOwner",
        title="Is Owner",
        description="""Is the attached driver is the owner of the registered vehicle. 
        Any base premium billing events will be charged to the driver who is the owner."""
    )
    is_default: bool = Field(
        default=False,
        alias="isDefault",
        title="Is Default",
        description="If this is the drivers default DRV, it will be their default vehicle for display and tracking purposes."
    )
    is_active: bool = Field(
        default=False,
        alias="isActive",
        title="Is Active",
        description="If this DRV is active. If not, then it will not be displayed and tracking cannot take place."
    )
    is_primary_driver: bool = Field(
        default=False,
        alias="isPrimaryDriver",
        title="Is Primary Driver",
        description="If this driver is the primary driver on this vehicle."
    )
    expires_at: Optional[datetime] = Field(
        default=None,
        alias="expiresAt",
        title="Expires At",
        description="""ISO timestamp of when this DRV expires. 
        Once expired, the isActive field is set to False. 
        This is useful for creating temporary access to a registered vehicle, eg. rental insurance. 
        If left as null, this DRV never expires.
        """
    )

    vehicle: Vehicle = Field(
        default=None,
        alias="registeredVehicle",
        title="Vehicle",
        description="The vehicle this DRV is associated with."
    )

    class Config:
        anystr_strip_whitespace = True

DriverVehicle.update_forward_refs()