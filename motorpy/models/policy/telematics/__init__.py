from pydantic import BaseModel, Field, conint, root_validator
from ..update import Mutable
from typing import Optional


class PolicyTelematicsBase(BaseModel, Mutable):
    telematics_policy_process: str = Field(
        default="indefinite",
        alias="process",
        title="Policy process",
        description="""Policy process.
If 'indefinite', then telematics is run indefinitely.
If 'days', then telematics is run for a specific number of days.
If 'min_km', then telematics is run for a specific number of km.
"""
    )
    telematics_days: Optional[conint(ge=0)] = Field(
        default=0,
        alias="days",
        title="Days",
        description="""Number of days of tracking before the policy is repriced."""
    )
    telematics_min_km: Optional[conint(ge=0)] = Field(
        default=0,
        alias="minKm",
        title="Min km",
        description="""Min KM needed before policy is repriced."""
    )


class PolicyTelematics(PolicyTelematicsBase):
    pass

    class Config:
        allow_population_by_field_name = True
