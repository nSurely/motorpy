from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class PolicyCancellationBase(BaseModel):
    cancellation_at: Optional[date] = Field(
        alias="cancelledAt",
        description="The date the policy was cancelled"
    )
    cancellation_message: Optional[str] = Field(
        alias="message",
        description="The reason for the cancellation"
    )


class PolicyCancellation(PolicyCancellationBase):
    pass

    class Config:
        allow_population_by_field_name = True

