import motorpy
import secrets
import pytest
import asyncio
from datetime import date


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

    async def test_create_driver(self, client: motorpy.Motor):
        new_driver = motorpy.Driver(
            first_name="John",
            last_name="Doe",
            email=secrets.token_hex(5) + "@example.com"
        )
        # print(new_driver.first_name)

        # export to pydantic dict
        driver_dict = new_driver.dict(exclude_unset=True, by_alias=True)
        print(driver_dict)

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

        await asyncio.sleep(2)

        # check driver is deleted
        with pytest.raises(motorpy.APIError) as excinfo:
            await client.get_driver(driver_id)
        assert excinfo.value.status_code == 404
