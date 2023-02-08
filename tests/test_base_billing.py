"Test the motorpy.Billing model"
import motorpy
import asyncio
import pytest
import pprint
from .helpers.compare import compare_dict_keys, flatten


class TestBilling:
    "Testing methods on the Billing model"

    pp = pprint.PrettyPrinter(indent=4)

    
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


    async def test_create_billing_event(self, driver: motorpy.Driver):
        new_billing_account_id = None
        new_ba_id = None
        try:
            # create a billing account
            new_ba = motorpy.BillingAccount(
                currency_iso_code="EUR",
                is_active=True,
                is_primary=True
            )
            new_ba = await driver.create_billing_account(new_ba)

            # list billing events
            await asyncio.sleep(2)

            # create a charge with a billing event object
            new_charge = motorpy.BillingEvent(
                amount=101,
                message="test",
                type="other"
            )
            new_charge = await driver.charge(
                event=new_charge
            )
            assert isinstance(new_charge, motorpy.BillingEvent)
            assert new_charge.amount == 101
            new_ba_id = new_charge.id
        finally:
            # clean up
            if new_ba_id:
                charge = await driver.get_charge(new_ba_id)
                await charge.update_status("cancelled")

            if new_billing_account_id:
                ba = await driver.get_billing_account(new_billing_account_id)
                await ba.delete(driver.id)

    async def test_billing_event_alias(self, driver: motorpy.Driver):
        # test alias functions
        events = [e async for e in driver.list_billing_events()]
        assert all(isinstance(e, motorpy.BillingEvent) for e in events)
        assert isinstance(events, list)

        if not events:
            return

        # use existing one
        be = await driver.get_billing_event(events[0].id)
        assert isinstance(be, motorpy.BillingEvent)
        # also test get charge
        be = await driver.get_charge(events[0].id)
        assert isinstance(be, motorpy.BillingEvent)