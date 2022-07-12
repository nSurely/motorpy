from pydantic import BaseModel, Field, confloat, conint
from ..enums import PaymentFrequency
from ..update import Mutable


class PolicyRatesBase(BaseModel, Mutable):
    rates_active: bool = Field(
        default=False,
        alias="enabled",
        title="Rates active",
        description="""Rate charging is enabled or not.  
If false, then rates are not UBI and driver is not charged on a per km basis.
"""
    )
    rates_value: confloat(ge=0.0) = Field(
        default=0.0,
        alias="value",
        title="Rates value",
        description="""Rates value in cents per km."""
    )
    rates_max: confloat(ge=0.0) = Field(
        default=0.0,
        alias="max",
        title="Rates max",
        description="""Rates max in cents per km. In the case of dynamic pricing, this is the maximum value of the rate."""
    )
    rates_min: confloat(ge=0.0) = Field(
        default=0.0,
        alias="min",
        title="Rates min",
        description="""Rates min in cents per km. In the case of dynamic pricing, this is the minimum value of the rate."""
    )
    rates_max_chargeable_distance_km: conint(ge=0) = Field(
        default=500,
        alias="chargeableDistanceKm",
        title="Rates max chargeable distance km",
        description="""Rates max chargeable distance km. This is the maximum distance at which the rate is charged for a single trip."""
    )
    rates_payment_frequency: PaymentFrequency = Field(
        default=PaymentFrequency.LAST_BUSINESS_DAY_OF_WEEK,
        alias="frequency",
        title="Rates payment frequency",
        description="""Rates payment frequency."""
    )
    rates_variable: bool = Field(
        default=False,
        alias="variable",
        title="Rates variable",
        description="""Rates variable or not.
If true, then rates can vary(dynamic risk).
"""
    )


class PolicyRates(PolicyRatesBase):
    pass

    class Config:
        allow_population_by_field_name = True
