from pydantic import BaseModel, Field, confloat
from ..update import Mutable

class PolicyNoClaimsBase(BaseModel, Mutable):
    no_claims_forgiveness: bool = Field(
        default=False,
        alias="forgiveness",
        description="Whether the policy has no claims forgiveness"
    )
    no_claims_discount_pc: confloat(ge=0.0, le=100.0) = Field(
        default=0.0,
        alias="discountPc",
        description="The percentage of the policy premium that is discounted for no claims. This is applied to the final premium"
    )


class PolicyNoClaims(PolicyNoClaimsBase):
    pass

    class Config:
        allow_population_by_field_name = True
