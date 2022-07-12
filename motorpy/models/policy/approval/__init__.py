from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from ..update import Mutable


class PolicyApprovalBase(BaseModel, Mutable):
    approved_at: Optional[datetime] = Field(
        default=None,
        alias="approvedAt",
        description="When the policy was approved in UTC"
    )
    auto_approved: bool = Field(
        default=False,
        alias="autoApproved",
        description="If the policy has been approved without manual approval."
    )
    approval_by: Optional[UUID] = Field(
        default=None,
        alias="approvedBy",
        description="The user who approved the policy"
    )


class PolicyApproval(PolicyApprovalBase):
    pass

    class Config:
        allow_population_by_field_name = True

    def is_approved(self):
        return self.approved_at is not None or self.auto_approved is True
