from pydantic import BaseModel, Field, conint, confloat
from typing import Optional
from ..update import Mutable


class PolicyFinalRates(BaseModel, Mutable):
    final_rates_value: confloat(ge=0.0) = Field(
        default=0.0,
        alias="value",
        description="""The final rate value after all factors have been applied.
In the case where variable rates are off, this is the only value to be applied to rates."""
    )
    final_rates_max: confloat(ge=0.0) = Field(
        default=0.0,
        alias="max",
        description="""The maximum rate value that can be applied."""
    )
    final_rates_min: confloat(ge=0.0) = Field(
        default=0.0,
        alias="min",
        description="""The minimum rate value that can be applied."""
    )
    final_rates_applied_risk_multiplier: Optional[confloat(ge=0.0)] = Field(
        default=None,
        alias="appliedRiskMultiplier",
        description="""The inherited relative weighted risk multiplier applied to value the time of policy generation."""
    )

    class Config:
        allow_population_by_field_name = True


class PolicyFinalPremium(BaseModel):
    final_base_premium_value: conint(ge=0) = Field(
        default=0,
        alias="value",
        description="""The final base premium value after all factors have been applied.
In the case where variable base premium is off, this is the only value to be applied to base premium."""
    )
    final_base_premium_applied_risk_multiplier: Optional[confloat(ge=0.0)] = Field(
        default=None,
        alias="appliedRiskMultiplier",
        description="""The inherited relative weighted risk multiplier applied to value the time of policy generation."""
    )

    class Config:
        allow_population_by_field_name = True


class PolicyFinalPricingBase(BaseModel, Mutable):
    requires_reprice: bool = Field(
        default=False,
        alias="requiresReprice",
        description="""If true, the policy needs to be repriced."""
    )
    final_rates: PolicyFinalRates = Field(
        default=PolicyFinalRates(),
        alias="rates",
        description="""The final rates applied to the policy."""
    )
    final_base_premium: PolicyFinalPremium = Field(
        default=PolicyFinalPremium(),
        alias="premium",
        description="""The final base premium applied to the policy."""
    )


class PolicyFinalPricing(PolicyFinalPricingBase):
    pass

    class Config:
        allow_population_by_field_name = True
