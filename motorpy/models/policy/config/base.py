from pydantic import BaseModel, Field
from ..enums import ISOCurrencyCode


class PolicyConfigStandardBase(BaseModel):
    display: str = Field(
        default=None,
        alias="display",
        title="Display",
        description="""Display name of the policy."""
    )
    description: str = Field(
        default=None,
        alias="description",
        title="Description",
        description="""Description of the policy."""
    )
    currency: ISOCurrencyCode = Field(
        default="EUR",
        alias="currency",
        title="Currency",
        description="""Currency of the policy."""
    )


class PolicyConfigStandardRead(PolicyConfigStandardBase):
    pass

    class Config:
        allow_population_by_field_name = True
