import motorpy.core as core
from motorpy.auth import Auth
from typing import Generator


class Vehicles(core.MotorBase):

    def __init__(self, org_id: str, auth: Auth, region: str = None, url: str = None) -> None:
        super().__init__(org_id, auth, region, url)

    def get_vehicle(self,
                    vehicle_id: str,
                    include_translations: bool = True,
                    include_distance: bool = False,
                    include_drv_count: bool = False) -> dict:
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

        return self.api.request("GET", f"registered-vehicles/{vehicle_id}", params=params)

    def search_vehicles(self,
                        reg_plate: str = None,
                        vin: str = None,
                        is_active: bool = None,
                        is_approved: bool = None,
                        full_response: bool = True) -> Generator[dict, None, None]:
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

        yield from self.api.batch_fetch("registered-vehicles", params=params)
