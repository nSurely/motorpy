from pydantic import BaseModel, Field, confloat
from ..update import Mutable

class PolicyRewardsRatesBase(BaseModel, Mutable):
    rewards_rates_active: bool = Field(
        default=False,
        alias="enabled",
        description="Rewards on rates are active and will be applied if this policy is active. This applies reward discounts on consilidated trip costs (UBI)."
    )
    rewards_rates_max_discount_pc: confloat(ge=0.0) = Field(
        default=20.0,
        alias="maxDiscountPc",
        description="Maximum discount percentage on rewards on rates"
    )

    class Config:
        allow_population_by_field_name = True
