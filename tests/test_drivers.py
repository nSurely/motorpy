"Test the motorpy.Driver model"
import motorpy
import asyncio
import pytest
import pprint
from .helpers.compare import compare_dict_keys, flatten


class TestDrivers:
    "Testing methods on the Driver model"

    pp = pprint.PrettyPrinter(indent=4)

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

    def test_driver_display_name(self):
        driver = motorpy.Driver(
            first_name="John",
            middle_name="Doe",
            last_name="Smith"
        )
        assert driver.get_display() == "John Doe Smith"
        assert driver.get_display() == driver.full_name

        # no middle name
        driver = motorpy.Driver(
            first_name="John",
            last_name="Smith"
        )
        assert driver.get_display() == "John Smith"
        assert driver.get_display() == driver.full_name

    def test_telematics_id_prop(self):
        _id = "1234567890"
        driver = motorpy.Driver(
            source_id=_id,
        )
        assert driver.telematics_id == _id

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

    async def test_driver_charge(self, driver: motorpy.Driver):
        new_billing_account_id = None
        new_charge_id = None
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

            # create a simple charge
            new_charge = await driver.charge(
                amount=100
            )
            assert isinstance(new_charge, motorpy.BillingEvent)
            assert new_charge.amount == 100
            new_charge_id = new_charge.id

            events = [e async for e in driver.list_charges()]
            assert all(isinstance(e, motorpy.BillingEvent) for e in events)
            assert isinstance(events, list)
        finally:
            if new_charge_id:
                charge = await driver.get_charge(new_charge_id)
                await charge.update_status("cancelled")

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

    # fleets
    async def test_fleet_list(self, driver: motorpy.Driver):
        fleets = await driver.list_fleets()
        if not fleets:
            return
        assert all([isinstance(f, motorpy.Fleet) for f in fleets])
        assert isinstance(fleets, list)

    # policies
    async def test_policy_list(self, driver: motorpy.Driver):
        policies = [p async for p in driver.list_policies()]
        if not policies:
            return
        assert all([isinstance(p, motorpy.Policy) for p in policies])
        assert isinstance(policies, list)

    async def test_policy_create(self, driver: motorpy.Driver):
        new_policy_id = None
        try:
            # create a policy
            new_policy = motorpy.Policy(
                sum_insured=1001
            )
            new_policy = await driver.create_policy(new_policy)
            assert isinstance(new_policy, motorpy.Policy)
            assert new_policy.id is not None
            assert new_policy.sum_insured == 1001
            new_policy_id = new_policy.id
        finally:
            # clean up
            if new_policy_id:
                policy = await driver.get_policy(new_policy_id)
                await policy.delete()

    # vehicles
    async def test_vehicle_list(self, driver: motorpy.Driver):
        vehicles = await driver.list_vehicles()
        if not vehicles:
            return
        assert all([isinstance(v, motorpy.DriverVehicle) for v in vehicles])
        assert isinstance(vehicles, list)

    @pytest.mark.skip(reason="not implemented")
    async def test_api_values(self, client: motorpy.Motor, driver: motorpy.Driver):
        driver_id = driver.id

        # should match the API json
        driver_model_dict = driver.dict(
            exclude_unset=False,
            by_alias=True,
            exclude={"api", "vehicles_raw"}
        )

        # get the driver from the API
        driver_api = await client.request(
            "GET",
            f"/drivers/{driver_id}",
            params={
                "policies": "t",
                "risk": "t",
                "address": "t",
                "fleets": "t",
                "vehicleCount": "t",
                "distance": "t",
                "files": "t",
                "contact": "t",
                "occupation": "t",
                "points": "t"
            }
        )

        if 'policies' in driver_api:
            # different implementation of the API
            del driver_api['policies']

        # self.pp.pprint(driver_model_dict.get("risk"))
        # self.pp.pprint(driver_model_dict)
        # self.pp.pprint(driver.risk)

        if not compare_dict_keys(driver_model_dict, driver_api):
            flat_driver_model_dict = flatten(driver_model_dict)
            flat_driver_api = flatten(driver_api)

            # self.pp.pprint(flat_driver_model_dict)

            _api_missing_keys = set(flat_driver_model_dict.keys()) - \
                set(flat_driver_api.keys())
            _model_missing_keys = set(flat_driver_api.keys()) - \
                set(flat_driver_model_dict.keys())

            print("\nAPI missing keys:")
            self.pp.pprint('None' if not _api_missing_keys else _api_missing_keys)
            print("\nModel missing keys:")
            self.pp.pprint('None' if not _model_missing_keys else _model_missing_keys)
            assert False
