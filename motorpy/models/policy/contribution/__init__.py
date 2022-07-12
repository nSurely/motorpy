from pydantic import BaseModel, Field
from typing import Optional
from ..update import Mutable


class PolicyContributionBase(BaseModel, Mutable):
    contribution_pc: float = Field(
        default=100.00,
        alias="pc",
        description="The percentage of the policy that is contributed by the insurer"
    )
    contribution_details: Optional[dict] = Field(
        alias="details",
        description="Additional details for external systems on contribution"
    )


class PolicyContribution(PolicyContributionBase):
    pass

    class Config:
        allow_population_by_field_name = True

