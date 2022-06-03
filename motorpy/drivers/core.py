import core
import models
from auth import Auth
from typing import Union

class Drivers(core.MotorBase):

    def __init__(self, org_id: str, auth: Auth, region: str = None, url: str = None) -> None:
        super().__init__(org_id, auth, region, url)

    def get_driver(self,
                   driver_id: str,
                   risk: bool = True,
                   address: bool = True,
                   fleets: bool = True,
                   vehicle_count: bool = False,
                   distance: bool = False,
                   points: bool = True,
                   files: bool = True,
                   contact: bool = True,
                   occupation: bool = True,
                   raw_output: bool = False,
                   **query) -> models.Driver:
        """Get a driver record.

        Args:
            driver_id (str): the UUID of the driver.
            risk (bool, optional): whether to include risk data. Defaults to True.
            address (bool, optional): whether to include address data. Defaults to True.
            fleets (bool, optional): whether to include fleet data. Defaults to True.
            vehicle_count (bool, optional): whether to include vehicle count data. Defaults to False.
            distance (bool, optional): whether to include distance data. Defaults to False.
            points (bool, optional): whether to include points data. Defaults to True.
            files (bool, optional): whether to include files data. Defaults to True.
            contact (bool, optional): whether to include contact data. Defaults to True.
            occupation (bool, optional): whether to include occupation data. Defaults to True.
            raw_output (bool, optional): whether to return the raw output (dict) or model. Defaults to False.
            **query (dict): additional query parameters.

        Returns:
            models.Driver: the driver model.
        """
        params = {
            **query,
            'risk': risk,
            'address': address,
            'fleets': fleets,
            'vehicleCount': vehicle_count,
            'distance': distance,
            'points': points,
            'files': files,
            'contact': contact,
            'occupation': occupation
        }

        driver_raw = self.api.request(
            "GET", f"drivers/{driver_id}", params=params
        )
        
        model: models.Driver = models.Driver.from_dict(driver_raw)

        model._api = self.api

        return model
