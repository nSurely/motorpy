import api
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List


class CustomBaseModel(BaseModel):
    def dict(self, **kwargs):
        hidden_fields = set(
            attribute_name
            for attribute_name, model_field in self.__fields__.items()
            if model_field.field_info.extra.get("hidden") is True
        )
        kwargs.setdefault("exclude", hidden_fields)
        return super().dict(**kwargs)


class Driver(CustomBaseModel):
    # private
    _api: api.APIHandler = Field(
        default=None,
        hidden=True
    )

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
    risk: Optional[dict] = Field(
        default=None,
        alias="risk"
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

    fleets: Optional[List[dict]] = Field(
        default_factory=list,
        alias="fleets"
    )

    def to_dict(self, api_format: bool = False, **kwargs):
        return self.dict(exclude={"_api"}, by_alias=api_format)

    def _check_id(self) -> None:
        """Check that the driver has an ID."""
        if not self.id:
            raise ValueError("Driver id is required")

    def list_billing_accounts(self, primary_only: bool = False) -> List[dict]:
        """List billing accounts for this driver.

        Args:
            primary_only (bool, optional): only return the primary account. Defaults to False.

        Returns:
            List[dict]: billing accounts
        """
        self._check_id()
        return self._api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/",
            params={
                "primary": primary_only,
            }
        )

    def get_billing_account(self, id: str) -> dict:
        """Get a billing account for this driver.

        Args:
            id (str): the id of the billing account

        Returns:
            dict: billing account
        """
        self._check_id()
        if not id:
            raise ValueError("Billing account id is required")
        return self._api.request(
            "GET",
            f"/drivers/{self.id}/billing-accounts/{id}"
        )

    def get_primary_billing_account(self) -> Optional[dict]:
        """Find the primary billing account for this driver.

        Returns:
            Optional[dict]: primary billing account
        """
        res: List[dict] = self.list_billing_accounts(primary_only=True)
        # make another request for the full account details
        return self.get_billing_account(res[0].get('id')) if res else None
