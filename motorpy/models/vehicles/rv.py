import motorpy.models as models
from pydantic import Field
from typing import Optional, Generator
from motorpy.models import PrivateAPIHandler
from datetime import datetime
from motorpy.models.risk import CommonRisk
from .v import VehicleType


class Vehicle(PrivateAPIHandler, CommonRisk):
    id: str = Field(
        default=None,
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
    
    def get_display(self) -> str:
        "A simple display string to identify the model to the user."
        if self.vehicle_type:
            return f"{self.vehicle_type.get_display()} - {self.reg_plate}"
        return self.reg_plate or "Unknown"
    
    @property
    def telematics_id(self) -> str:
        """
        Return the telematics ID.

        Returns:
            str: telematics ID
        """
        return self.source_id

    async def list_policies(self, is_active_policy: bool = None) -> Generator['models.policies.Policy', None, None]:
        """List policies for this vehicle.

        Args:
            is_active_policy (bool, optional): if True, will return only active policies. Defaults to None.

        Returns:
            Generator[Policy]: policies
        """
        params = {
            "rvIds": self.id
        }
        if is_active_policy is not None:
            params["isActivePolicy"] = is_active_policy

        async for p in self.api.batch_fetch(f"policy", params=params):
            yield models.policies.Policy(api=self.api, **p)

    async def create_policy(self, policy: 'models.policies.Policy' = None) -> 'models.policies.Policy':
        """Create a policy for this vehicle.

        Args:
            policy (Policy): policy to create. This can be left None and a new policy will be created using the org defaults.

        Returns:
            Policy: created policy
        """
        if policy is None:
            policy = models.policies.Policy(api=self.api)
        policy.policy_group = 'rv'
        return await policy.create(
            api_handler=self.api,
            record_id=self.id,
        )
    
    async def add_drv(self, driver_id: str, drv: 'models.vehicles.DriverVehicle') -> 'models.vehicles.DriverVehicle':
        """Add a driver to this vehicle.

        Args:
            driver_id (str): driver ID
            drv (DriverVehicle): driver vehicle to add

        Returns:
            DriverVehicle: added driver vehicle
        """
        if not drv.api:
            drv.api = self.api
        return await drv.create(driver_id)

    
    async def add_driver(self, driver_id: str, display_name: str, is_owner: bool, is_primary_driver: bool) -> 'models.vehicles.DriverVehicle':
        """Add a driver to this vehicle.

        Args:
            driver_id (str): driver ID
            display_name (str): display name
            is_owner (bool): is owner
            is_primary_driver (bool): is primary driver

        Returns:
            DriverVehicle: added driver vehicle
        """
        drv = models.vehicles.DriverVehicle(
            api=self.api,
            display_name=display_name,
            is_owner=is_owner,
            is_primary_driver=is_primary_driver
        )
        return await self.add_drv(driver_id, drv)
    
    def _check_id(self) -> None:
        if not self.id:
            raise ValueError("id must be set.")

    async def refresh(self) -> None:
        """
        Refresh the model from the API.
        """
        self._check_id()
        api = self.api
        self.__init__(
            **(await self.api.request("GET",
                               f"/registered-vehicles/{self.id}")),
            api=api
        )

    async def delete(self) -> None:
        """
        Delete this record via the API.
        """
        self._check_id()
        await self.api.request(
            "DELETE",
            f"/registered-vehicles/{self.id}"
        )

    async def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return await self._save(
            url=f"/registered-vehicles/{self.id}",
            fields=fields,
            exclude={'vehicle_type'}
        )

    async def update(self, persist: bool = False, **kwargs) -> None:
        """
        Update a field on the model, call save or keyword persist to persist changes in the API.

        Args:
            persist (bool): whether to persist the changes to the API. Defaults to False.
            **kwargs: the model fields to update.

        Note: when doing multiple updates, it is recommended to call update() after all updates are made.
        """
        await self._update(persist=persist, **kwargs)
