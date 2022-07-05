import pprint
import pytest
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
