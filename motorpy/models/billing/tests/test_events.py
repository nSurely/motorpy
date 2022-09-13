from motorpy import models
from datetime import datetime, date


class TestBillingEvent:

    def test_model_init(self):
        _ = models.billing.events.BillingEvent(
            id="123",
            external_id="123",
            payment_id="123",
            amount=123,
            message="123",
            payment_out=True,
            payment_date=datetime(2020, 1, 1),
            status="pending",
            approval_at=datetime(2020, 1, 1),
            policy_id="123",
            type="other",
            created_at=datetime(2020, 1, 1),
            billing_account=models.billing.accounts.BillingAccount(
                external_id="123",
                expiry=date(2020, 1, 1),
                updated_at=datetime(2020, 1, 1),
                is_active=True,
                is_primary=True,
                created_at=datetime(2020, 1, 1),
                currency_iso_code="USD",
                country_iso_code="US",
                address_line_1="123",
                address_line_2="123",
                address_line_3="123",
                county="123",
                province="123",
                postcode="123",
            ),
        )

    def test_json_format_init(self):
        event = models.billing.events.BillingEvent(**{
            "externalId": "string",
            "paymentId": "string",
            "amount": 0,
            "message": "string",
            "paymentOut": False,
            "paymentDate": "2019-08-24T14:15:22Z",
            "status": "pending",
            "approvalAt": "2019-08-24T14:15:22Z",
            "policyId": "string",
            "type": "base_premium",
            "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
            "createdAt": "2019-08-24T14:15:22Z",
            "billingAccount": {
                    "adrLine1": "string",
                    "adrLine2": "string",
                    "adrLine3": "string",
                    "county": "string",
                    "province": "string",
                    "postcode": "string",
                    "externalId": "string",
                    "adrSameAsHome": True,
                    "expiry": "2019-08-24",
                    "updatedAt": "2019-08-24T14:15:22Z",
                    "isActive": True,
                    "isPrimary": True,
                    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
                    "createdAt": "2019-08-24T14:15:22Z",
                    "countryIsoCode": "ie",
                    "currencyIsoCode": "eur"
            },
            "approvalBy": "47eb095b-854a-411f-a1da-947f3174ed23"
        })

        assert event.get_currency() == "eur"
        assert event.is_approved() == True
