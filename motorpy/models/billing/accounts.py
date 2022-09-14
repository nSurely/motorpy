import motorpy.models as models
from pydantic import Field, BaseModel, PaymentCardNumber, constr
from typing import Optional
from datetime import date, datetime


class Card(BaseModel):
    name: Optional[constr(strip_whitespace=True, min_length=1)] = Field(
        default=None,
        alias="name",
        description="""
The name of the cardholder.

> This data is retained."""
    )
    number: Optional[PaymentCardNumber] = Field(
        default=None,
        alias="number",
        description="""
The card number, as a string of digits.

> This data is deleted after 3 hours.
"""
    )
    expiry: Optional[date] = Field(
        default=None,
        alias="exp",
        description="""
Expiration date of the card.

> This data is deleted after 3 hours.
"""
    )
    cvv: Optional[constr(strip_whitespace=True, min_length=3, max_length=4)] = Field(
        default=None,
        alias="cvv",
        description="""
The CVV code, as a string of digits.

> This data is deleted after 3 hours.
"""
    )
    last_four: Optional[constr(strip_whitespace=True, min_length=4, max_length=4)] = Field(
        default=None,
        alias="lastFour",
        description="""
The last four digits of the card number. This is set from the card number when the card is created.

> This data is retained.
"""
    )
    added_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        alias="updatedAt",
        description="""
The date and time the card was added/updated.

> This data is retained.
"""
    )
    third_party_id: Optional[constr(max_length=256)] = Field(
        default=None,
        alias="thirdPartyId",
        description="""
The third party identifier for the card.

> This data is retained.
"""
    )


class BillingAccount(models.PrivateAPIHandler):
    # identifiers
    id: str = Field(
        None,
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
        default=None,
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

    card: Optional[Card] = Field(
        default=None,
        alias="card",
        title="Card",
        description="The card details for this billing account. Card number, cvv and expiry are deleted after 3 hours."
    )

    class Config:
        allow_population_by_field_name = True

    def get_display(self) -> str:
        "A simple display string to identify the model to the user."
        if not self.card:
            return "Unknown"
        return f"{'Primary ' if self.is_primary else ''}{self.card.card_name} - {self.card.card_last_four}"
