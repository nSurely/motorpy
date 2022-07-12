from pydantic import BaseModel, Field, confloat
from ..update import Mutable


class PolicyRewardsPremiumBase(BaseModel, Mutable):
    rewards_base_premium_active: bool = Field(
        default=False,
        alias="enabled",
        description="Rewards on premium are active and will be applied if this policy is active. This applies reward discounts on base premium amounts."
    )
    rewards_base_premium_max_discount_pc: confloat(ge=0.0) = Field(
        default=20.0,
        alias="maxDiscountPc",
        description="Maximum discount percentage on rewards on premium"
    )

    class Config:
        allow_population_by_field_name = True
