from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class PolicyApprovalBase(BaseModel):
    approval_approved_at: Optional[datetime] = Field(
        default=None,
        alias="approvedAt",
        description="When the policy was approved in UTC"
    )
    approval_auto_approved: bool = Field(
        default=False,
        alias="autoApproved",
        description="If the policy has been approved without manual approval."
    )
    approval_by: Optional[UUID] = Field(
        default=None,
        alias="approvedBy",
        description="The user who approved the policy"
    )

    def apply_approval(self, requires_approval: bool = True) -> None:
        """Sets the approval fields based on whether the policy requires approval or not
        """
        print("apply_approval")
        print(self)
        print(requires_approval)
        if not requires_approval:
            # automatically sets to approved if approval not required
            self.approval_auto_approved = True
            self.approval_approved_at = datetime.utcnow()
            self.approval_by = None
            self.__fields_set__.add('approval_auto_approved')
            self.__fields_set__.add('approval_approved_at')
            self.__fields_set__.add('approval_by')
        print(self)


class PolicyApproval(PolicyApprovalBase):
    pass

    class Config:
        allow_population_by_field_name = True

