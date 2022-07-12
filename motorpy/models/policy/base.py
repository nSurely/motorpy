from pydantic import BaseModel, Field, conint, conset
from datetime import datetime
from .enums.cover import PolicyCoverType
from .enums.group import PolicyGroup


class PolicyBase(BaseModel):
    "The base policy model. All other models should be nested in a seprate model that inherits this one."
    uid: str = Field(
        default=None,
        alias="id",
        description="The unique identifier for this policy"
    )
    created_at: datetime = Field(
        default=None,
        alias="createdAt",
        description="The date and time this policy record was created"
    )
    policy_group: PolicyGroup = Field(
        default=None,
        alias="policyGroup",
        description="The policy group this policy belongs to"
    )
    is_active: bool = Field(
        default=True,
        alias="isActivePolicy",
        description="""If the policy is the active to be used for pricing.  

This field is useful when constructing a multi-use policy, such as a vehicle with an owner who is traditional insurance, and a named driver on UBI.

> Note: The end-user still may see this record. This field is just used for pricing.        
"""
    )
    sum_insured: conint(ge=0) = Field(
        default=0,
        alias="sumInsured",
        description="The maximum sum insured on this policy"
    )
    can_renew: bool = Field(
        default=True,
        alias="canRenew",
        description="If the policy can be renewed. If not the policy must be cancelled and a new record with a new policy ID created."
    )
    cover_type: conset(PolicyCoverType, min_items=1) = Field(
        default={PolicyCoverType.COMPREHENSIVE},
        alias="cover",
        description="The cover types for this policy"
    )
    max_passengers: conint(ge=0) = Field(
        default=1,
        alias="maxPassengers",
        description="The maximum number of passengers that can be covered by this policy. This may not apply to all cover types."
    )

    class Config:
        allow_population_by_field_name = True
