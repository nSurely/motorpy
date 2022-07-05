"""
This test covers the API handler class as it is inherited by many models.
"""
from ..accounts import BillingAccount


class TestApiHandler:

    def test_export_hidden_attributes(self):
        """
        Test that the API handler class exports the correct hidden attributes.
        """
        b = BillingAccount(
            id="123",
        )

        assert hasattr(b, "api")

        export = b.dict()
        assert "api" not in export
        # assert "api" not in str(b.__str__)
        # assert "api" not in str(b.__repr__)
