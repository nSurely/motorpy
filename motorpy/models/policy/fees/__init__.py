from pydantic import BaseModel, Field, conint
from ..update import Mutable


class PolicyFeesBase(BaseModel, Mutable):
    fees_cancellation: conint(ge=0) = Field(
        default=0,
        alias="cancellation",
        description="Fees for cancellation before expiry"
    )
    fees_renewal: conint(ge=0) = Field(
        default=0,
        alias="renewal",
        description="Fees for when expiry lapses and is renewed"
    )
    fees_new_business: conint(ge=0) = Field(
        default=0,
        alias="newBusiness",
        description="Fees for brand new policy"
    )


class PolicyFees(PolicyFeesBase):
    pass

    class Config:
        allow_population_by_field_name = True
