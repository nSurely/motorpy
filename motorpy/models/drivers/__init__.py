import motorpy.models as models
from pydantic import Field, parse_obj_as
from datetime import datetime, date
from typing import Optional, List
# from motorpy.models.billing import BillingAccount
# from motorpy.models.fleets import Fleet
# from motorpy.models.risk import Risk


class Driver(models.custom.PrivateAPIHandler, models.risk.CommonRisk):
    # identifiers
    id: str = Field(
        ...,
        description="The driver's unique ID.",
    )
    source_id: Optional[str] = Field(
        default=None
    )
    external_id: Optional[str] = Field(
        default=None
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

    # implementing fleets using a property to avoid circular imports
    fleet_raw: List[dict] = Field(
        default=[],
        alias="fleets"
    )

    vehicles_raw: List[dict] = Field(
        default=[],
        alias="fleets"
    )

    @property
    def vehicles(self) -> List['models.vehicles.DriverVehicle']:
        """List vehicles for this driver.

        Returns:
            List[DriverVehicle]: vehicles
        """
        if not self.vehicles_raw:
            self.vehicles_raw = self.api.request(
                "GET", f"drivers/{self.id}/vehicles")
        return [models.vehicles.DriverVehicle(api=self.api, **v) for v in (self.vehicles_raw or [])]

    def to_dict(self, api_format: bool = False, **kwargs):
        return self.dict(exclude={"api"}, by_alias=api_format)

    def _check_id(self) -> None:
        """Check that the driver has an ID."""
        if not self.id:
            raise ValueError("Driver id is required")

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

    def list_billing_accounts(self, primary_only: bool = False) -> List[models.billing.BillingAccount]:
        """List billing accounts for this driver.

        Args:
            primary_only (bool, optional): only return the primary account. Defaults to False.

        Returns:
            List[BillingAccount]: billing accounts
        """
        self._check_id()
        accounts = self.api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/",
            params={
                "primary": primary_only,
            }
        )
        return [models.billing.BillingAccount(api=self.api, **ba) for ba in (accounts or [])]

    @property
    def billing_accounts(self) -> List[models.billing.BillingAccount]:
        """List billing accounts for this driver.

        Returns:
            List[BillingAccount]: billing accounts
        """
        return self.list_billing_accounts()

    def get_billing_account(self, id: str) -> models.billing.BillingAccount:
        """Get a billing account for this driver.

        Args:
            id (str): the id of the billing account

        Returns:
            BillingAccount: billing account
        """
        self._check_id()
        if not id:
            raise ValueError("Billing account id is required")
        return models.billing.BillingAccount(api=self.api, **self.api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/{id}"
        ))

    def get_primary_billing_account(self) -> Optional[models.billing.BillingAccount]:
        """Find the primary billing account for this driver.

        Returns:
            Optional[BillingAccount]: primary billing account
        """
        res: List[models.billing.BillingAccount] = self.list_billing_accounts(
            primary_only=True)
        # make another request for the full account details
        return self.get_billing_account(res[0].id) if res else None

    @property
    def primary_billing_account(self) -> Optional[models.billing.BillingAccount]:
        """Find the primary billing account for this driver.

        Returns:
            Optional[BillingAccount]: primary billing account
        """
        return self.get_primary_billing_account()

    # fleets

    @property
    def fleets(self) -> List['models.fleets.Fleet']:
        """List fleets for this driver.

        Returns:
            List[Fleet]: fleets
        """
        if not self.fleet_raw:
            return []
        return [models.fleets.Fleet(api=self.api, **f) for f in (self.fleet_raw or [])]

    @fleets.setter
    def fleets(self, fleets: List['models.fleets.Fleet']) -> None:
        """Set the fleets for this driver. This will call the API foreach fleet to get all fields unless specified otherwise."""
        self.fleet_raw = [f.to_dict(by_alias=True) for f in fleets]

    # policies
    def vehicle_policies(self, vehicle_id: str) -> List['models.policies.Policy']:
        """List policies for this driver.

        Returns:
            List[Policy]: policies
        """
        return [models.policies.Policy(api=self.api, **p) for p in (self.api.request(
                "GET", f"drivers/{self.id}/vehicles/{vehicle_id}/policy"
                ) or [])]


Driver.update_forward_refs()
