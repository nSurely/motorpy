import motorpy
import secrets
import pytest
from datetime import date


def test_base_name():
    assert motorpy.base.NAME == "motorpy"

class TestBaseDrivers:
    "Testing driver methods on base client"

    async def test_list_drivers(self, client: motorpy.Motor):
        drivers = [d async for d in client.list_drivers(max_records=1)]
        assert len(drivers) == 1
    
    async def test_driver_search(self, client: motorpy.Motor):
        drivers = [d async for d in client.list_drivers(
            first_name=motorpy.Search("joe", "ilike"),
            dob=motorpy.Search(date(1942, 11, 20), "eq"),
            max_records=10
        )]
        assert len(drivers) > 0

        assert drivers[0].first_name.lower() == "joe"

    async def test_get_driver(self, client: motorpy.Motor):
        drivers = [d async for d in client.list_drivers(max_records=1)]
        assert len(drivers) == 1

        driver = await client.get_driver(drivers[0].id)
        assert driver.id == drivers[0].id
    
    @pytest.skip("Not implemented")
    async def test_create_driver(self, client: motorpy.Motor):
        new_driver = motorpy.Driver(
            first_name="John",
            last_name="Doe",
            email=secrets.token_hex(10) + "@example.com"
        )

        print(new_driver.__fields_set__)
        print(new_driver.dict(exclude_unset=True, by_alias=True))

        driver = await client.create_driver(
            driver=new_driver,
            password=secrets.token_hex(16),
            send_invite=False,
            send_webhook=False
        )

        driver_id = driver.id
        assert driver.id is not None
        assert driver.first_name == "John"
        assert driver.last_name == "Doe"
        assert driver.email == new_driver.email

        # delete driver
        await driver.delete()

        # check driver is deleted
        try:
            await client.get_driver(driver_id)
        except motorpy.APIError as e:
            assert e.not_found
        else:
            assert False, "Driver should not exist"