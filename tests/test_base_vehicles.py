import motorpy
import pytest
import asyncio
import random


class TestBaseVehicles:
    "Testing driver methods on base client"

    async def test_list_vehicles(self, client: motorpy.Motor):
        vehicles = [d async for d in client.list_vehicles(max_records=1)]
        assert len(vehicles) == 1

    async def test_vehicle_search(self, client: motorpy.Motor):
        vehicles = [d async for d in client.list_vehicles(max_records=10)]
        assert len(vehicles) > 0

        # pick from 10 random vehicles
        rand_v: motorpy.Vehicle = random.choice(vehicles)

        # get registration and vin for search
        reg_plate = rand_v.reg_plate.lower()
        vin = rand_v.vin.lower()

        vehicles = [v async for v in client.list_vehicles(
            reg_plate=motorpy.Search(reg_plate, "ilike"),
            vin=motorpy.Search(vin, "ilike"),
        )]
        assert len(vehicles) > 0

        assert vehicles[0].vin.lower() == vin
        assert vehicles[0].reg_plate.lower() == reg_plate

    async def test_get_vehicle(self, client: motorpy.Motor):
        vehicles = [d async for d in client.list_vehicles(max_records=1)]
        assert len(vehicles) == 1

        vehicle = await client.get_vehicle(vehicles[0].id)
        assert vehicle.id == vehicles[0].id

        assert isinstance(vehicle, motorpy.Vehicle)

    async def test_list_vehicle_types(self, client: motorpy.Motor):
        vehicle_types = [d async for d in client.list_vehicle_types()]
        assert len(vehicle_types) > 0

        assert isinstance(vehicle_types[0], motorpy.VehicleType)

    async def test_create_vehicle_type(self, client: motorpy.Motor):
        new_vehicle_type = motorpy.VehicleType(
            description="Test Vehicle Type Description",
            brand="Ford",
            model="Fiesta",
        )

        vehicle_type = await client.create_vehicle_type(
            vehicle_type=new_vehicle_type,
        )

        vehicle_type_id = vehicle_type.id
        assert vehicle_type.id is not None
        assert vehicle_type.description == "Test Vehicle Type Description"
        assert vehicle_type.brand == "Ford"
        assert vehicle_type.model == "Fiesta"

        # delete vehicle type
        await vehicle_type.delete()

        await asyncio.sleep(2)

        # check vehicle type is deleted
        with pytest.raises(motorpy.APIError) as excinfo:
            await client.get_vehicle_type(vehicle_type_id)
        assert excinfo.value.status_code == 404

    async def test_create_vehicle(self, client: motorpy.Motor):
        # create vehicle type
        new_vehicle_type = motorpy.VehicleType(
            description="Test Vehicle Type Description",
            brand="Ford",
            model="Fiesta",
        )

        vehicle_type = await client.create_vehicle_type(
            vehicle_type=new_vehicle_type,
        )

        vehicle_type_id = vehicle_type.id

        # create vehicle
        new_vehicle = motorpy.Vehicle(
            reg_plate="ABC123",
            vin="12345678901234567",
            vehicle_type=motorpy.VehicleType(id=vehicle_type_id),
        )

        vehicle = await client.create_vehicle(
            vehicle=new_vehicle,
        )

        vehicle_id = vehicle.id
        assert vehicle.id is not None
        assert vehicle.reg_plate == "ABC123"
        assert vehicle.vin == "12345678901234567"

        # delete vehicle
        await vehicle.delete()
        await vehicle_type.delete()
        
        # wait for delete to complete
        await asyncio.sleep(2)

        # check vehicle is deleted
        with pytest.raises(motorpy.APIError) as excinfo:
            await client.get_vehicle(vehicle_id)
        assert excinfo.value.status_code == 404
