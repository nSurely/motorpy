from pydantic import BaseModel, Field, conint
from datetime import datetime, timedelta
from typing import Optional
from ..update import Mutable


class PolicyDurationBase(BaseModel,Mutable):
    start: datetime = Field(
        default_factory=lambda: datetime.utcnow(),
        alias="start",
        description="The start date of the policy"
    )
    end: Optional[datetime] = Field(
        alias="end",
        description="The end date of the policy. If not set, the policy is open ended"
    )
    grace_period_mins: conint(ge=0) = Field(
        default=0,
        alias="gracePeriodMins",
        description="The number of minutes after the policy end timestamp that the policy is still active"
    )


class PolicyDuration(PolicyDurationBase):
    pass

    class Config:
        allow_population_by_field_name = True

    def is_expired(self):
        return self.end is not None and (self.end + timedelta(minutes=self.grace_period_mins)) < datetime.utcnow()
