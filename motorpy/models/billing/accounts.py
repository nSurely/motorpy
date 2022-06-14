import models
from pydantic import Field
from typing import Optional
from datetime import date, datetime


class BillingAccount(models.PrivateAPIHandler):
    # identifiers
    id: str = Field(
        ...,
        description="The billing account's unique ID.",
    )
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId",
    )
    expiry: Optional[date] = Field(
        default=None,
        alias="expiry",
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        alias="updatedAt",
    )
    is_active: bool = Field(
        default=False,
        alias="isActive",
    )
    is_primary: bool = Field(
        default=False,
        alias="isPrimary",
    )
    created_at: datetime = Field(
        alias="createdAt",
    )
    currency_iso_code: Optional[str] = Field(
        default=None,
        alias="currencyIsoCode",
    )
    country_iso_code: Optional[str] = Field(
        default=None,
        alias="countryIsoCode",
    )
    # address
    address_line_1: Optional[str] = Field(
        default=None,
        alias="adrLine1",
    )
    address_line_2: Optional[str] = Field(
        default=None,
        alias="adrLine2",
    )
    address_line_3: Optional[str] = Field(
        default=None,
        alias="adrLine3",
    )
    county: Optional[str] = Field(
        default=None,
        alias="county",
    )
    province: Optional[str] = Field(
        default=None,
        alias="province",
    )
    postcode: Optional[str] = Field(
        default=None,
        alias="postcode",
    )
    country_name: Optional[str] = Field(
        default=None,
        alias="countryName",
    )
    # status
    third_party_id: Optional[str] = Field(
        default=None,
        alias="thirdPartyId",
        description="The third party ID for the billing account, eg. Stripe account ID.",
    )

    class Config:
        allow_population_by_field_name = True
