from pydantic import BaseModel, Field
from ..enums import ISOCurrencyCode
from ..update import Mutable


class PolicyConfigStandardBase(BaseModel, Mutable):
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


class PolicyConfigStandard(PolicyConfigStandardBase):
    pass

    class Config:
        allow_population_by_field_name = True
