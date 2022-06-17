"""
This test covers the API handler class as it is inherited by many models.
"""
from ..accounts import BillingAccount
import api
import auth


class TestApiHandler:

    def test_export_hidden_attributes(self):
        """
        Test that the API handler class exports the correct hidden attributes.
        """
        b = BillingAccount(
            id="123",
        )

        assert hasattr(b, "_api")

        export = b.dict()
        assert "_api" not in export
        assert "_api" not in str(b.__str__)
        assert "_api" not in str(b.__repr__)
