from pydantic import BaseModel, Field
from ..update import Mutable

# * generation


class PolicyGenerationBase(BaseModel, Mutable):
    generation_max_passengers_inherit_vehicle: bool = Field(
        default=False,
        alias="maxPassengersInheritVehicle",
        description="""Set max passengers to inherit vehicle seats amount."""
    )
    generation_auto_issued: bool = Field(
        default=False,
        alias="autoIssued",
        description="""
If the policy is autogenerated when a new record is added.  
If true, then the policy will be automatically issued based on risk inheritance and policy defaults.
"""
    )

    class Config:
        allow_population_by_field_name = True


class PolicyGeneration(PolicyGenerationBase):
    pass

    class Config:
        allow_population_by_field_name = True
