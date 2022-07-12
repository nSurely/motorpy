from pydantic import BaseModel, Field, conint
from ..enums import PaymentFrequency
from datetime import date
from typing import Optional
from ..update import Mutable


class PolicyBasePremiumBase(BaseModel, Mutable):
    base_premium_value: conint(ge=0) = Field(
        default=0,
        alias="value",
        title="Base premium value",
        description="""Base premium value in cents per payment cycle."""
    )
    base_premium_payable_immediate: bool = Field(
        default=True,
        alias="payableImmediate",
        title="Base premium payable immediate",
        description="""Base premium payable immediate or not.
If true, then the total will be billed based on the payment frequency.
"""
    )
    base_premium_frequency: Optional[PaymentFrequency] = Field(
        default=PaymentFrequency.LAST_BUSINESS_DAY_OF_YEAR,
        alias="frequency",
        title="Base premium frequency",
        description="""Base premium frequency."""
    )
    base_premium_use_frequency: bool = Field(
        default=False,
        alias="useFrequency",
        title="Base premium use frequency",
        description="""Base premium use frequency or not.
If true, then the payment frequency will be used.
"""
    )
    base_premium_next_payment_date: date = Field(
        default=None,
        alias="nextPaymentDate",
        title="Base premium next payment date",
        description="""Base premium next payment date."""
    )
    base_premium_variable: bool = Field(
        default=False,
        alias="variable",
        title="Base premium variable",
        description="""Base premium variable or not.
If true, then the base premium can vary(dynamic risk).
"""
    )


class PolicyBasePremium(PolicyBasePremiumBase):
    pass

    class Config:
        allow_population_by_field_name = True
