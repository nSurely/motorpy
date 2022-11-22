import motorpy
import pytest


class TestBaseFleets:
    "Testing driver methods on base client"

    async def test_list_fleets(self, client: motorpy.Motor):
        fleets = [d async for d in client.list_fleets(max_records=1)]
        assert len(fleets) == 1
    
    async def test_get_fleet(self, client: motorpy.Motor):
        fleets = [d async for d in client.list_fleets(max_records=1)]
        assert len(fleets) == 1
    
        fleet = await client.get_fleet(fleets[0].id)
        assert fleet.id == fleets[0].id
    
    async def test_create_fleet(self, client: motorpy.Motor):
        new_fleet = motorpy.Fleet(
            display="Test Fleet",
            description="Test Fleet Description"
        )
        # print(new_driver.first_name)
    
        # export to pydantic dict
        fleet_dict = new_fleet.dict(exclude_unset=True, by_alias=True)
        print(fleet_dict)
    
        fleet = await client.create_fleet(
            fleet=new_fleet
        )
    
        fleet_id = fleet.id
        assert fleet.id is not None
        assert fleet.display == "Test Fleet"
        assert fleet.description == "Test Fleet Description"
    
        # delete fleet
        await fleet.delete()
    
        # check fleet is deleted
        with pytest.raises(motorpy.APIError) as excinfo:
            await client.get_fleet(fleet_id)
        assert excinfo.value.status_code == 404