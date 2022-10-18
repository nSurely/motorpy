import motorpy.models as models
from motorpy.api import APIHandler
from typing import Generator


class Vehicles:

    def __init__(self, api: APIHandler) -> None:
        self.api = api

    async def get_vehicle(self,
                    vehicle_id: str,
                    include_translations: bool = True,
                    include_distance: bool = False,
                    include_drv_count: bool = False) -> models.Vehicle:
        """Get a registered vehicle record.

        Args:
            vehicle_id (str): the UUID of the vehicle.
            include_translations (bool, optional): whether to include translations. Defaults to True.
            include_distance (bool, optional): whether to include distance. Defaults to False.
            include_drv_count (bool, optional): whether to include driver count. Defaults to False.

        Returns:
            dict: the vehicle record.
        """
        params = {}
        params['drv'] = 't'
        params['trns'] = 't' if include_translations else 'f'
        params['distance3m'] = 't' if include_distance else 'f'
        params['totalDrvCount'] = 't' if include_drv_count else 'f'

        return models.Vehicle(api=self.api, **(await self.api.request("GET", f"registered-vehicles/{vehicle_id}", params=params)))

    async def list_vehicles(self,
                      reg_plate: str = None,
                      vin: str = None,
                      is_active: bool = None,
                      is_approved: bool = None,
                      full_response: bool = True,
                      max_records: int = None) -> Generator[models.Vehicle, None, None]:
        """Search for registered vehicles.

        Args:
            reg_plate (str, optional): the registration plate. Defaults to None.
            vin (str, optional): the VIN. Defaults to None.
            is_active (bool, optional): whether to search for active vehicles. Defaults to None.
            is_approved (bool, optional): whether to search for approved vehicles. Defaults to None.
            full_response (bool, optional): whether to return full response. Defaults to True.

        Returns:
            dict: the vehicle record.
        """
        params = {}

        if reg_plate:
            params["regPlate"] = reg_plate
        if vin:
            params["vin"] = vin
        if is_active is not None:
            params["isActive"] = is_active
        if is_approved is not None:
            params["isApproved"] = is_approved

        params['full'] = 't' if full_response else 'f'

        count = 0
        async for vehicle in self.api.batch_fetch("registered-vehicles", params=params):
            if max_records is not None:
                if count >= max_records:
                    break
            model: models.Vehicle = models.Vehicle(**vehicle, api=self.api)
            yield model
            count += 1

    async def create_vehicle(self, vehicle: models.Vehicle, driver_id: str = None, drv: models.DriverVehicle = None, send_webhook: bool = True) -> models.Vehicle:
        """Create a new vehicle.

        Args:
            vehicle (models.Vehicle): the vehicle model.

        Returns:
            models.Vehicle: the created vehicle model.
        """
        raw = await self.api.request("POST", 
        "registered-vehicles", 
        json=vehicle.dict(exclude_unset=True),
        params={
            "webhook": "t" if send_webhook else "f"
        })

        rv: models.Vehicle = models.Vehicle(**raw, api=self.api)

        # create a DRV
        try:
            if driver_id:
                if not drv:
                    await rv.add_driver(driver_id, display_name=rv.get_display(), is_owner=True, is_primary_driver=True)
                else:
                    await rv.add_drv(driver_id, drv)
        except Exception as e:
            # rollback
            await self.api.request("DELETE", f"registered-vehicles/{rv.id}")
            raise e

        return rv