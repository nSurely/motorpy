from datetime import datetime
from pydantic import Field
from typing import Optional
from ..frequent import APIPath
from .enums import PolicyGroup


class PolicySearch(APIPath):
    "Search Fields on DRV policies"
    uid: str = Field(
        default=None,
        alias="id",
        description="Policy UID"
    )
    display: str = Field(
        default=None,
        alias="display",
        description="Policy display name"
    )
    approval_approved_at: Optional[datetime] = Field(
        default=None,
        alias="approvedAt",
        description="Approval timestamp"
    )
    cancellation_at: Optional[datetime] = Field(
        default=None,
        alias="cancelledAt",
        description="Cancellation timestamp"
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt",
        description="Creation timestamp"
    )
    policy_type: PolicyGroup = Field(
        default=None,
        alias="policyType",
        description="Policy type"
    )

    class Config:
        allow_population_by_field_name = True
