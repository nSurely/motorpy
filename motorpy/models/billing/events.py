from motorpy.models import PrivateAPIHandler
from motorpy.models.billing.accounts import BillingAccount
from pydantic import Field
from typing import Optional, Literal
from datetime import datetime

STATUS = {
    'pending',
    'paid',
    'failed',
    'cancelled',
    'confirmed'
}

BillingEventStatus = Literal[
    'pending',
    'paid',
    'failed',
    'cancelled',
    'confirmed'
]

BillingEventType = Literal[
    'other',
    'rates',
    'base_premium'
]

class BillingEvent(PrivateAPIHandler):
    # identifiers
    id: str = Field(
        ...,
        description="The billing event's unique ID.",
    )
    external_id: Optional[str] = Field(
        default=None,
        alias="externalId",
    )
    payment_id: Optional[str] = Field(
        default=None,
        alias="paymentId",
    )
    amount: int = Field(
        default=0,
        alias="amount",
    )
    message: Optional[str] = Field(
        default=None,
        alias="message",
    )
    payment_out: bool = Field(
        default=False,
        alias="paymentOut",
    )
    payment_date: Optional[datetime] = Field(
        default=None,
        alias="paymentDate",
    )
    status: Optional[BillingEventStatus] = Field(
        default=None,
        alias="status",
    )
    approval_at: Optional[datetime] = Field(
        default=None,
        alias="approvalAt",
    )
    policy_id: Optional[str] = Field(
        default=None,
        alias="policyId",
    )
    type: Optional[BillingEventType] = Field(
        default=None,
        alias="type",
    )
    created_at: Optional[datetime] = Field(
        default=None,
        alias="createdAt",
    )
    billing_account: "Optional[BillingAccount]" = Field(
        default=None,
        alias="billingAccount",
    )
    approval_by: Optional[str] = Field(
        default=None,
        alias="approvalBy",
    )

    class Config:
        allow_population_by_field_name = True

    def get_currency(self) -> Optional[str]:
        "Get the ISO currency code for the billing event."
        if self.billing_account:
            return self.billing_account.currency_iso_code
        return None

    def is_approved(self) -> bool:
        "Check if the billing event has been approved."
        return self.approval_at is not None

    def update(self, data: dict) -> None:
        "Update the billing event."
        self._api.request(
            'PATCH',
            f'/billing-events/{self.id}',
            data=data
        )

    def update_status(self, status: str, payment_id: str = None) -> None:
        "Update the status of the billing event. Optionally add a payment ID."
        if status not in STATUS:
            raise ValueError(
                f"Invalid status: {status} - can only be one of {STATUS}")

        data = {
            "status": status,
        }

        if payment_id:
            data["paymentId"] = payment_id

        # update via API
        self.update(data)
        # if API call was successful, update the object
        self.status = status


# update forwards refs
BillingEvent.update_forward_refs()
