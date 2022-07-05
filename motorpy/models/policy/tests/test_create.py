import pprint
from datetime import datetime, timedelta
from ..nested import Policy
from .const import FULL, ORG_CONF

pp = pprint.PrettyPrinter(indent=4)


class TestCreate:
    def test_create_basic(self):
        to_test = {
            "id": "DRV-123",
            "createdAt": "2020-01-01T00:00:00.000Z",
            "isActivePolicy": True,
            "sumInsured": 100.00,
            "canRenew": True,
            "cover": [
                "comprehensive"
            ],
            "maxPassengers": 1
        }
        p = Policy(**to_test)

        assert p.is_active == True
        assert p.sum_insured == 100.00
        assert p.can_renew == True
        assert p.cover_type == {'comprehensive'}
        assert p.max_passengers == 1

    def test_create_nested(self):
        _ = Policy(**FULL)

    def test_is_live(self):
        p = Policy(**FULL)

        assert p.is_live() == False

        p.approval.approved_at = datetime.now()
        p.cancellation.cancellation_at = None
        p.duration.end = datetime.now() + timedelta(days=1)
        p.driver.driver_policy_agreed_at = datetime.now()

        assert p.is_live() == True

    def test_sub_bools(self):
        p = Policy(**{
            'id': 'DRV-123',
            'createdAt': '2020-01-01T00:00:00.000Z',
        })
        print(p.approval)
        assert p.is_approved() == False
        p.approval.approved_at = datetime.now()
        assert p.is_approved() == True

        assert p.is_cancelled() == False
        p.cancellation.cancellation_at = datetime.now()
        assert p.is_cancelled() == True
        p.cancellation.cancellation_at = None
        assert p.is_cancelled() == False

        assert p.is_expired() == False
        p.duration.end = datetime.now() - timedelta(days=30)
        assert p.is_expired() == True

        assert p.is_driver_agreed() == False
        p.driver.driver_policy_agreed_at = datetime.now()
        assert p.is_driver_agreed() == True
