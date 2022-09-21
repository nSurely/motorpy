import motorpy.models as models
from pydantic import Field, validator, parse_raw_as, parse_obj_as
from datetime import datetime, date
from typing import Optional, List, Generator, Any

from motorpy.models.billing.events import BillingEvent, BillingEventStatus, BillingEventType


class Driver(models.custom.PrivateAPIHandler, models.risk.CommonRisk):
    """
    The Driver object, representing a driver in the API.  
    Billing accounts, vehicles and more can be accessed via the Driver object.
    """
    # identifiers
    id: str = Field(
        None,
        description="The driver's unique ID.",
    )
    source_id: Optional[str] = Field(
        default=None,
        alias="sourceId"
    )
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId"
    )

    # personal
    first_name: str = Field(
        default=None,
        alias="firstName",
    )
    middle_name: Optional[str] = Field(
        default=None,
        alias="middleName",
    )
    last_name: str = Field(
        default=None,
        alias="lastName",
    )
    gender: Optional[str] = Field(
        default=None,
        alias="gender"
    )
    email: str = Field(
        default=None,
        alias="email"
    )
    phone: Optional[str] = Field(
        default=None,
        alias="telE164"
    )
    date_of_birth: date = Field(
        default=None,
        alias="dob"
    )
    language: Optional[str] = Field(
        default=None,
        alias="lang"
    )
    driving_start_date: date = Field(
        default=None,
        alias="drivingStartDate"
    )
    occupation: dict = Field(
        default=None,
        alias="occupation"
    )

    api_path: Optional[str] = Field(
        default=None,
        alias="apiPath"
    )

    # address
    address_line_1: Optional[str] = Field(
        default=None,
        alias="adrLine1"
    )
    address_line_2: Optional[str] = Field(
        default=None,
        alias="adrLine2"
    )
    address_line_3: Optional[str] = Field(
        default=None,
        alias="adrLine3"
    )
    county: Optional[str] = Field(
        default=None,
        alias="county"
    )
    province: Optional[str] = Field(
        default=None,
        alias="province"
    )
    postcode: Optional[str] = Field(
        default=None,
        alias="postcode"
    )
    country_iso_code: Optional[str] = Field(
        default=None,
        alias="countryIsoCode"
    )
    country_name: Optional[str] = Field(
        default=None,
        alias="countryName"
    )

    # status
    approved_at: Optional[datetime] = Field(
        default=None,
        alias="approvedAt"
    )
    activation_id: Optional[str] = Field(
        default=None,
        alias="activationId"
    )
    driver_activated: Optional[bool] = Field(
        default=None,
        alias="driverActivated"
    )
    activated_at: Optional[datetime] = Field(
        default=None,
        alias="activatedAt"
    )
    is_approved: bool = Field(
        default=False,
        alias="isApproved"
    )
    is_active: bool = Field(
        default=False,
        alias="isActive"
    )

    # files
    drivers_license_file_location: Optional[str] = Field(
        default=None,
        alias="driversLicenseLoc"
    )
    proof_of_address_file_location: Optional[str] = Field(
        default=None,
        alias="proofOfAddressLoc"
    )
    id_file_location: Optional[str] = Field(
        default=None,
        alias="idLoc"
    )
    profile_pic_file_location: Optional[str] = Field(
        default=None,
        alias="profilePicLoc"
    )

    # nested
    vehicle_count: int = Field(
        default=0,
        alias="vehicleCount"
    )

    # meta
    total_points: Optional[int] = Field(
        default=None,
        alias="totalPoints"
    )
    month_distance: Optional[int] = Field(
        default=None,
        alias="distanceKm30Days"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt"
    )

    # circular reference
    # see validator for more info
    fleets: List[Any] = Field(
        default_factory=list,
        alias="fleets"
    )

    @validator('fleets')
    def set_fleets(cls, value: List[Any]) -> List[Any]:
        """Set the fleets for this driver.

        Args:
            value (List[Any]): fleets
        """
        if not value:
            return []
        # parse json if applicable
        # cast to FleetDriver models
        if isinstance(value, (str, bytes)):
            value = parse_raw_as(List[models.fleets.FleetDriver], value)
        elif isinstance(value, list):
            value = parse_obj_as(List[models.fleets.FleetDriver], value)
        for f in value:
            f.driver = cls
            f.api = cls.api
        return value

    vehicles_raw: List[dict] = Field(
        default=[]
    )

    async def list_vehicles(self) -> List[models.vehicles.DriverVehicle]:
        """List all vehicles for this driver.

        Returns:
            List[Vehicle]: list of vehicles
        """
        self.vehicles_raw = await self.api.request("GET",
                                                   f"drivers/{self.id}/vehicles")
        return [models.vehicles.DriverVehicle(api=self.api, **v) for v in self.vehicles_raw]

    def to_dict(self, api_format: bool = False, **kwargs):
        return self.dict(exclude={"api"}, by_alias=api_format)

    def get_display(self) -> str:
        "A simple display string to identify the model to the user."
        return self.full_name()

    def _check_id(self) -> None:
        """Check that the driver has an ID."""
        if not self.id:
            raise ValueError("Driver id is required")

    @property
    def telematics_id(self) -> str:
        """
        Return the telematics ID.

        Returns:
            str: telematics ID
        """
        return self.source_id

    @property
    def full_name(self) -> str:
        """Get the driver's full name.

        Returns:
            str: full name
        """
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    # billing

    async def list_billing_accounts(self, primary_only: bool = False) -> List[models.billing.BillingAccount]:
        """List billing accounts for this driver.

        Args:
            primary_only (bool, optional): only return the primary account. Defaults to False.

        Returns:
            List[BillingAccount]: billing accounts
        """
        self._check_id()
        accounts = await self.api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/",
            params={
                "primary": primary_only,
            }
        )
        return [models.billing.BillingAccount(api=self.api, **ba) for ba in (accounts or [])]

    async def get_billing_account(self, id: str) -> models.billing.BillingAccount:
        """Get a billing account for this driver.

        Args:
            id (str): the id of the billing account

        Returns:
            BillingAccount: billing account
        """
        self._check_id()
        if not id:
            raise ValueError("Billing account id is required")
        return models.billing.BillingAccount(api=self.api, **(await self.api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/{id}"
        )))

    async def get_primary_billing_account(self) -> Optional[models.billing.BillingAccount]:
        """Find the primary billing account for this driver.

        Returns:
            Optional[BillingAccount]: primary billing account
        """
        res: List[models.billing.BillingAccount] = await self.list_billing_accounts(
            primary_only=True)
        # make another request for the full account details
        return await self.get_billing_account(res[0].id) if res else None
    
    async def create_billing_account(self, account: models.billing.BillingAccount) -> models.billing.BillingAccount:
        """Create a billing account for this driver.

        Args:
            account (BillingAccount): the account to create

        Returns:
            BillingAccount: the created account
        """
        self._check_id()
        return models.billing.BillingAccount(api=self.api, **(await self.api.request(
            "POST",
            f"/drivers/{self.id}/billing-accounts",
            json=account.to_dict(exclude_unset=True)
        )))

    async def charge(self, amount: int = None, event: BillingEvent = None) -> BillingEvent:
        """Charge the driver. The billing event will be entered under their current primary billing account.

        Args:
            amount (int, optional): the amount to charge. Defaults to None.
            event (BillingEvent, optional): the billing event to charge. This overrides the amount if both are provided. Defaults to None.

        Raises:
            ValueError: if neither amount nor event are provided

        Returns:
            BillingEvent: the billing event
        """
        if not amount and not event:
            raise ValueError("Either amount or event is required")

        if not event:
            event = BillingEvent(
                amount=amount,
                description="Charge",
                type="other",
            )

        self._check_id()
        return models.billing.BillingEvent(api=self.api, **(await self.api.request(
            "POST",
            f"/drivers/{self.id}/billing-events",
            json=event.dict(exclude_unset=True)
        )))

    async def list_charges(self, event_type: BillingEventType = None, event_status: BillingEventStatus = None, max_records: int = None) -> Generator[BillingEvent, None, None]:
        """List all charges for this driver.
        
        Args:
            event_type (BillingEventType, optional): filter by type. Defaults to None.
            event_status (BillingEventStatus, optional): filter by status. Defaults to None.
            max_records (int, optional): maximum number of records to return. Defaults to None.

        Yields:
            Generator[BillingEvent, None, None]: billing events
        """
        self._check_id()

        params = {}
        if event_type:
            params["type"] = event_type
        if event_status:
            params["status"] = event_status

        count = 0
        async for p in self.api.batch_fetch(f"/drivers/{self.id}/billing-events", params=params):
            if max_records:
                if count >= max_records:
                    break
            yield models.policy.BillingEvent(api=self.api, **p)
            count += 1

    # fleets

    async def list_fleets(self) -> List['models.fleets.Fleet']:
        "List fleets for this driver."
        if not self.fleets:
            await self.refresh()
        fleets = []
        for fd in self.fleets:
            f = await fd.get_fleet()
            if f:
                fleets.append(f)
        return fleets

    # policies
    async def list_vehicle_policies(self, vehicle_id: str) -> List['models.policy.Policy']:
        """List policies for this driver.

        Returns:
            List[Policy]: policies
        """
        return [models.policies.Policy(api=self.api, **p) for p in (await self.api.request(
                "GET", f"policy", params={
                    "drvIds": vehicle_id
                }) or [])]

    async def list_policies(self, loose_match: bool = True, is_active_policy: bool = None) -> Generator['models.policy.Policy', None, None]:
        """List policies for this driver.

        Args:
            loose_match (bool, optional): if True, will return any policy related to the driver (D, DRV, RV, FD, FDRV). Defaults to True.
            is_active_policy (bool, optional): if True, will return only active policies. Defaults to None.

        Returns:
            Generator[Policy]: policies
        """
        params = {
            "driverIds": self.id,
            "driverLooseMatch": loose_match
        }
        if is_active_policy is not None:
            params["isActivePolicy"] = is_active_policy

        async for p in self.api.batch_fetch(f"policy", params=params):
            yield models.policy.Policy(api=self.api, **p)

    async def create_policy(self, policy: 'models.policy.Policy' = None) -> 'models.policy.Policy':
        """Create a policy for this driver.

        Args:
            policy (Policy): policy to create. This can be left None and a new policy will be created using the org defaults.

        Returns:
            Policy: created policy
        """
        if policy is None:
            policy = models.policy.Policy(api=self.api)
        policy.policy_group = 'd'
        return await policy.create(
            api_handler=self.api,
            record_id=self.id,
        )

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
                                      f"/drivers/{self.id}",
                                      params={
                                          "risk": True,
                                          "address": True,
                                          "fleets": True,
                                          "files": True,
                                          "contact": True,
                                          "occupation": True,
                                          "points": True,
                                          "policies": True
                                      })),
            api=api
        )

    async def delete(self) -> None:
        """
        Delete this record via the API.
        """
        self._check_id()
        await self.api.request(
            "DELETE",
            f"/drivers/{self.id}"
        )

    async def save(self, fields: dict = None) -> Optional[dict]:
        """
        Persist any changes in the API.

        Args:
            fields (dict, optional): the API formatted fields to update. If not supplied, any set fields in the model will be updated in the API. Defaults to None.
        """
        self._check_id()

        return await self._save(
            url=f"/drivers/{self.id}",
            fields=fields,
            exclude={'fleets', 'vehicles_raw', 'created_at'}
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

    async def list_trackable_models(self, fleet_id: str = None) -> List['models.TrackableAsset']:
        """List trackable models for this driver.

        Depending on the org settings, this will return a model that contains a source ID.
        The source ID (not the ID) will be used to identify the model for telematics.

        Args:
            fleet_id (str, optional): the fleet ID to filter on. Defaults to None.

        Returns:
            List[TrackableAsset]: assets that can be tracked for different insurance use-cases.
        """
        if not self.api.org_data:
            await self.api.refresh_org_data()

        # todo: check enforcements from org
        # todo: add enforcement to org

        # todo: list from policy general route

        sid_type = self.api.org_data.source_id_type

        assets: List['models.TrackableAsset'] = []

        if sid_type == 'drv':
            return [drv for drv in (await self.list_vehicles()) if drv.is_active]
        elif sid_type == 'rv':
            # returns only active RVs
            return [drv.vehicle for drv in (await self.list_vehicles()) if drv.is_active and drv.vehicle.is_active]
        elif sid_type == 'd':
            return [self]
        elif sid_type == 'fd':
            fleets = await self.list_fleets()
            if fleets:
                for fleet in fleets:
                    if fleet_id is not None:
                        if fleet.id != fleet_id:
                            continue
                    driver_record = await fleet.get_driver(self.id)
                    if driver_record:
                        assets.append(driver_record)
        elif sid_type == 'fdrv' or sid_type == 'frv':
            # frv and fdrvs will be returned here as 'open to all' frv's are returned as well
            fleets = await self.list_fleets()
            if fleets:
                for fleet in fleets:
                    if fleet_id is not None:
                        if fleet.id != fleet_id:
                            continue
                    async for fdrv in fleet.list_driver_vehicle_assignments(
                            self.id,
                            include_unassigned=(sid_type == 'frv')):
                        if sid_type == 'fdrv':
                            # only return fdrvs that are assigned to the driver and active
                            if fdrv.is_assigned and fdrv.is_active:
                                assets.append(fdrv.driver)
                                continue
                        else:
                            if not fdrv.is_assigned and fdrv.is_active:
                                assets.append(fdrv)
        return assets

    @property
    async def tracking_id(self) -> Optional[str]:
        """
        Get the tracking ID for this driver.

        Returns:
            str: tracking ID
        """
        assets = await self.list_trackable_models()
        if not assets:
            return None
        return assets[0].source_id


Driver.update_forward_refs()
