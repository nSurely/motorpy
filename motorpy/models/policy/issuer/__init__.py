from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from ..update import Mutable


class PolicyIssuerBase(BaseModel, Mutable):
    issuer_id: Optional[UUID] = Field(
        default=None,
        alias="id",
        description="The user who issued the policy"
    )
    issuer_policy_agreed_at: Optional[datetime] = Field(
        default=None,
        alias="policyAgreedAt",
        description="When the policy was agreed to by the issuer"
    )


class PolicyIssuer(PolicyIssuerBase):
    pass

    class Config:
        allow_population_by_field_name = True
