from pydantic import BaseModel, Field, conint, conset
from .enums import PolicyGroup, PolicyConfigTemplate, PolicyCoverType

from .config import PolicyConfig
from .contribution import PolicyContribution
from .excess import PolicyExcess
from .extras import PolicyExtrasNested
from .fees import PolicyFees
from .premium import PolicyBasePremium
from .rates import PolicyRates
from .rewards import PolicyRewards
from .telematics import PolicyTelematics


class PolicyOrgConfigBase(BaseModel):
    policy_group: PolicyGroup = Field(
        default=...,
        alias="group",
        title="Policy Group",
        description="""What policy record this config applies to."""
    )
    policy_config: PolicyConfigTemplate = Field(
        default="custom",
        alias="settings",
        title="Policy Settings",
        description="""Changing this value will automatically set specific fields to match this setting.  
For example, if set to 'ubi', the rates and telematics fields will be set to match a UBI policy.

> Note: By default, this is set to `custom` so values must be explicitly set.
"""
    )
    cover_type: conset(PolicyCoverType, min_items=1) = Field(
        default={PolicyCoverType.COMPREHENSIVE},
        alias="cover",
        description="The cover types for this policy"
    )
    assign_policy_on_create: bool = Field(
        default=False,
        alias="assignPolicyOnCreate",
        title="Assign Policy On Create",
        description="""If true, a policy will be assigned automatically to the record based on the defaults defined here."""
    )
    requires_approval: bool = Field(
        default=False,
        alias="requiresApproval",
        title="Requires Approval",
        description="""Must be manually approved by an admin before the policy is activated."""
    )
    valid_mins: conint(ge=1) = Field(
        default=None,
        alias="validMins",
        title="Valid Minutes",
        description="""Valid Minutes to Expiry.  
The number of minutes before the policy expires, when compared to the `duration.start` field on the policy.  
The `duration.end` field is calculated based on this value and the `duration.start` field.  

Minutes is the smallest unit of time available for a policy to be active.  
For example, if a policy is set to expire in 30 minutes, then the policy will be active for 30 minutes (short term insurance).  
If a policy is set to expire in 1 year, then the policy will be active for 525,600 minutes (traditional yearly insurance).  

> Note: If set to null, then the policy will be open ended and won't expire.
"""
    )
    duration_grace_period_mins: conint(ge=0) = Field(
        default=0,
        alias="gracePeriodMins",
        description="The number of minutes after the policy end timestamp that the policy is still active"
    )


class PolicyOrgConfigFlat(PolicyOrgConfigBase):
    pass

    class Config:
        allow_population_by_field_name = True


# * nested

class PolicyOrgConfig(PolicyOrgConfigFlat):
    config: PolicyConfig = Field(
        default=PolicyConfig(),
        alias="config",
        description="The configuration details for the policy"
    )
    contribution: PolicyContribution = Field(
        default=PolicyContribution(),
        alias="contribution",
        description="The contribution details for the policy"
    )
    excess: PolicyExcess = Field(
        default=PolicyExcess(),
        alias="excess",
        description="The excess details for the policy"
    )
    extras: PolicyExtrasNested = Field(
        default=PolicyExtrasNested(),
        alias="extras",
        description="The extras details for the policy"
    )
    fees: PolicyFees = Field(
        default=PolicyFees(),
        alias="fees",
        description="The fees details for the policy"
    )
    premium: PolicyBasePremium = Field(
        default=PolicyBasePremium(),
        alias="premium",
        description="The premium details for the policy"
    )
    rates: PolicyRates = Field(
        default=PolicyRates(),
        alias="rates",
        description="The rates details for the policy"
    )
    rewards: PolicyRewards = Field(
        default=PolicyRewards(),
        alias="rewards",
        description="The rewards details for the policy"
    )
    telematics: PolicyTelematics = Field(
        default=PolicyTelematics(),
        alias="telematics",
        description="The telematics details for the policy"
    )

    class Config:
        allow_population_by_field_name = True
