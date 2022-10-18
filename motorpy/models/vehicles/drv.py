import motorpy.models as models
from pydantic import Field
from typing import Optional, Generator
from motorpy.models import PrivateAPIHandler
from datetime import datetime
from motorpy.models.risk import CommonRisk
from .rv import Vehicle


class DriverVehicle(PrivateAPIHandler, CommonRisk):
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

    # not returned from the API, set manually
    driver_id: str = Field(
        default=None
    )

    class Config:
        allow_population_by_field_name = True
        anystr_strip_whitespace = True

    def get_display(self) -> str:
        "A simple display string to identify the model to the user."
        if self.vehicle:
            return f"{self.display_name} ({self.vehicle.get_display()})"
        return self.display_name or "Unknown"

    @property
    def telematics_id(self) -> str:
        """
        Return the telematics ID.

        Returns:
            str: telematics ID
        """
        return self.source_id
    
    async def get_vehicle(self) -> 'models.vehicles.Vehicle':
        """Get the vehicle associated with this DRV.

        Returns:
            Vehicle: vehicle
        """
        return models.vehicles.Vehicle(api=self.api, **(await self.api.request(
            method="GET",
            url=f"registered-vehicle/{self.vehicle.id}"
        )))

    async def list_policies(self,
                            loose_match: bool = True,
                            is_active_policy: bool = None,
                            max_records: int = None) -> Generator['models.policies.Policy', None, None]:
        """List policies for this vehicle.

        Args:
            loose_match: If True, will match on the DRV ID and the vehicle ID.
            is_active_policy (bool, optional): if True, will return only active policies. Defaults to None.
            max_records (int, optional): maximum number of records to return. Defaults to None.

        Returns:
            Generator[Policy]: policies
        """
        params = {
            "drvIds": self.id
        }
        if loose_match:
            params["rvIds"] = self.vehicle.id
        if is_active_policy is not None:
            params["isActivePolicy"] = is_active_policy
        
        count = 0

        async for p in self.api.batch_fetch(f"policy", params=params):
            if max_records is not None:
                if count >= max_records:
                    break
            yield models.policies.Policy(api=self.api, **p)
            count += 1

    async def create_policy(self, policy: 'models.policies.Policy' = None) -> 'models.policies.Policy':
        """Create a policy for this driver.

        Args:
            policy (Policy): policy to create. This can be left None and a new policy will be created using the org defaults.

        Returns:
            Policy: created policy
        """
        if policy is None:
            policy = models.policies.Policy(api=self.api)
        policy.policy_group = 'drv'
        return await policy.create(
            api_handler=self.api,
            record_id=self.id,
        )

    async def create(self, driver_id: str) -> 'models.vehicles.DriverVehicle':
        """Create a DRV.

        Args:
            driver_id (str): driver ID
            drv (DriverVehicle): DRV to create

        Returns:
            DriverVehicle: created DRV
        """
        return await self.api.request(
            method="POST",
            url=f"driver/{driver_id}/vehicles",
            json=self.dict(by_alias=True)
        )

    def _check_id(self) -> None:
        if not self.driver_id or not self.id:
            raise ValueError("Id and driver_id must be set.")

    async def refresh(self) -> None:
        """
        Refresh the model from the API.
        """
        self._check_id()
        api = self.api
        driver_id = self.driver_id
        self.__init__(
            **(await self.api.request("GET",
                                      f"/drivers/{self.driver_id}/vehicles/{self.id}")),
            api=api,
            driver_id=driver_id
        )

    async def delete(self) -> None:
        """
        Delete the driver vehicle via the API.
        """
        self._check_id()
        await self.api.request(
            "DELETE",
            f"/drivers/{self.driver_id}/vehicles/{self.id}"
        )

    async def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return await self._save(
            url=f"/drivers/{self.driver_id}/vehicles/{self.id}",
            fields=fields,
            exclude={'driver_id', 'vehicle'}
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


DriverVehicle.update_forward_refs()
