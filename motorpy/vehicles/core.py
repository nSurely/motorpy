import core
from auth import Auth
from typing import Generator


class Vehicles(core.MotorBase):

    def __init__(self, org_id: str, auth: Auth, region: str = None, url: str = None) -> None:
        super().__init__(org_id, auth, region, url)

    def get_vehicle(self, vehicle_id: str, **query) -> dict:
        """Get a registered vehicle record.

        Args:
            vehicle_id (str): the UUID of the vehicle.

        Returns:
            dict: the vehicle record.
        """
        return self.api.request("GET", f"registered-vehicles/{vehicle_id}", params=query)

    def search_vehicles(self,
                        reg_plate: str = None,
                        vin: str = None,
                        is_active: bool = None,
                        is_approved: bool = None,
                        full_response: bool = True) -> Generator[dict, None, None]:
        """Search for registered vehicles.

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
