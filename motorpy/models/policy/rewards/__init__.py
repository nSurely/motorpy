from pydantic import BaseModel, Field, conint
from .premium import PolicyRewardsPremiumBase
from .rates import PolicyRewardsRatesBase
from ..update import Mutable


class PolicyRewardsBase(BaseModel, Mutable):
    rewards_active: bool = Field(
        default=False,
        alias="enabled",
        description="Rewards are enabled and will be applied if this policy is active"
    )
    rewards_max_monthly: conint(ge=0) = Field(
        default=0,
        alias="maxMonthly",
        description="Maximum amount of monthly reward events"
    )

    # nested fields
    rates: PolicyRewardsRatesBase = Field(
        default=PolicyRewardsRatesBase(),
        alias="rates",
        description="Rates rewards config"
    )

    premium: PolicyRewardsPremiumBase = Field(
        default=PolicyRewardsPremiumBase(),
        alias="premium",
        description="Premium rewards config"
    )


class PolicyRewards(PolicyRewardsBase):
    pass

    class Config:
        allow_population_by_field_name = True
