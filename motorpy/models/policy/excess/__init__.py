from pydantic import BaseModel, Field, conint
from ..update import Mutable


class PolicyExcessBase(BaseModel, Mutable):
    excess_voluntary: conint(ge=0) = Field(
        default=0,
        alias="voluntary",
        description="""The voluntary excess amount."""
    )
    excess_compulsory: conint(ge=0) = Field(
        default=0,
        alias="compulsory",
        description="""The compulsory excess amount."""
    )


class PolicyExcess(PolicyExcessBase):
    pass

    class Config:
        allow_population_by_field_name = True

