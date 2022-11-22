"Test the motorpy.Driver model"
import motorpy
import asyncio
import pytest
from datetime import date


class TestDrivers:
    "Testing methods on the Driver model"

    async def test_driver_display(self, driver: motorpy.Driver):
        display = driver.get_display()
        assert display == driver.full_name
        assert display == (f"{driver.first_name} {driver.last_name}"
                           if not driver.middle_name
                           else f"{driver.first_name} {driver.middle_name} {driver.last_name}")

    async def test_driver_list_vehicle(self, driver: motorpy.Driver):
        vehicles = await driver.list_vehicles()
        if len(vehicles) > 0:
            assert all(isinstance(v, motorpy.DriverVehicle) for v in vehicles)
        assert isinstance(vehicles, list)

    async def test_driver_billing_accounts(self, driver: motorpy.Driver):
        new_billing_account_id = None
        try:
            # create a billing account
            new_ba = motorpy.BillingAccount(
                currency_iso_code="EUR",
                is_active=True,
            )
            new_ba = await driver.create_billing_account(new_ba)

            assert isinstance(new_ba, motorpy.BillingAccount)
            assert new_ba.currency_iso_code == "EUR"
            assert new_ba.is_active is True
            assert new_ba.id is not None
            new_billing_account_id = new_ba.id

            # list billing accounts
            await asyncio.sleep(2)
            accounts = await driver.list_billing_accounts()
            assert all(isinstance(a, motorpy.BillingAccount) for a in accounts)

            # check new is there
            # assert any(True for a in accounts if a.id == new_billing_account_id)

            # get a billing account
            account = accounts[0]
            ba = await driver.get_billing_account(account.id)
            assert isinstance(ba, motorpy.BillingAccount)

            # get the primary billing account
            primary = await driver.get_primary_billing_account()
            assert isinstance(primary, motorpy.BillingAccount)
            assert primary.is_primary is True

            assert isinstance(accounts, list)
        finally:
            # clean up
            if new_billing_account_id:
                ba = await driver.get_billing_account(new_billing_account_id)
                await ba.delete(driver.id)
