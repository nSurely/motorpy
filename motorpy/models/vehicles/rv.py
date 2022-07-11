from pydantic import Field
from typing import Optional
from motorpy.models import PrivateAPIHandler
from datetime import datetime
from motorpy.models.risk import CommonRisk
from .v import VehicleType


class Vehicle(PrivateAPIHandler, CommonRisk):
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

    # files API
    front_pic_loc: Optional[str] = Field(
        default=None,
        alias="frontPicLoc",
        title="Front Image of Vehicle - File"
    )
    side_pic_loc_1: Optional[str] = Field(
        default=None,
        alias="sidePicLoc1",
        title="Side Image of Vehicle (1 of 2) - File"
    )
    side_pic_loc_2: Optional[str] = Field(
        default=None,
        alias="sidePicLoc2",
        title="Side Image of Vehicle (2 of 2) - File"
    )
    rear_pic_loc: Optional[str] = Field(
        default=None,
        alias="rearPicLoc",
        title="Rear Image of Vehicle - File"
    )
    top_pic_loc: Optional[str] = Field(
        default=None,
        alias="topPicLoc",
        title="Top Image of Vehicle - File"
    )
    por_loc: Optional[str] = Field(
        default=None,
        alias="proofOfRegLoc",
        title="Proof of Registration - File",
        description="Scan of proof of registration of this vehicle. For any operations on this file, use the `/file*` routes."
    )

    distance_3m: float = Field(
        default=0.0,
        alias="distance3m",
        title="Distance (3m)",
        description="The distance in KM from the last 3 months, including all DRV's."
    )
    total_drv_count: int = Field(
        default=0,
        alias="totalDrvCount",
        title="Total DRV Count",
        description="The total number of DRV's that have been associated with this vehicle."
    )
    reg_plate: Optional[str] = Field(
        default=None,
        alias="regPlate",
        title="Registration Number",
        description="The vehicle registration plate number."
    )
    vin: Optional[str] = Field(
        default=None,
        alias="vin",
        title="VIN",
        description="The vehicle identification number."
    )
    year: Optional[int] = Field(
        default=None,
        alias="year",
        title="Year of Production.",
        description="The year this vehicle was produced."
    )
    preowned: Optional[bool] = Field(
        default=None,
        alias="preowned",
        title="Is Preowned",
        description="If this vehicle has had previous owner(s)."
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
    on_road_parking: Optional[bool] = Field(
        default=None,
        alias="onRoadParking",
        title="Is Parked On Road Side",
        description="If this vehicle is parked on an active roadway."
    )
    mileage_km: Optional[int] = Field(
        default=None,
        alias="mileageKm",
        title="Mileage (KM)",
        description="The most recent odometer reading in KM."
    )
    engine_litres: Optional[float] = Field(
        default=None,
        alias="engineLitres",
        title="Engine Capacity Litres",
        description="The engine capacity in litres. This value overrides the inherited vehicle value."
    )
    fuel_type: Optional[str] = Field(
        default=None,
        alias="fuelType",
        title="Fuel Type",
        description="The vehicle fuel type. This value overrides the inherited vehicle value."
    )
    has_turbo: Optional[bool] = Field(
        default=None,
        alias="hasTurbo",
        title="Turbocharger",
        description="If this vehicle has been modified to have a turbocharger."
    )
    has_supercharger: Optional[bool] = Field(
        default=None,
        alias="hasSupercharger",
        title="Supercharger",
        description="If this vehicle has been modified to have a supercharger.")
    body_modified: Optional[bool] = Field(
        default=None,
        alias="bodyModified",
        title="Body Modified",
        description="If the body of this vehicle has been modified from its stock option."
    )
    engine_modified: Optional[bool] = Field(
        default=None,
        alias="engineModified",
        title="Engine Modified",
        description="If the engine of this vehicle has been modified from its stock option."
    )
    # colors_id: Optional[bool] = Field(None, alias="colorsId")
    gearbox_type: Optional[str] = Field(
        default=None,
        alias="gearboxType",
        title="Gearbox Type",
        description="The gearbox type. This value overrides the inherited vehicle value."
    )
    is_active: bool = Field(
        default=True,
        alias="isActive",
        title="Is Active",
        description="If this vehicle is active. If false, this vehicle will not be returned to the end user."
    )

    vehicle_type: Optional[VehicleType] = Field(
        default=None,
        alias="vehicle",
        title="Vehicle Type",
        description="The vehicle type."
    )

    class Config:
        allow_population_by_field_name = True
        anystr_strip_whitespace = True