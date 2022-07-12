import motorpy.models as models
from motorpy.api import APIHandler
from datetime import date
from typing import Union, Generator
import motorpy.search as search


class Drivers:

    def __init__(self, api: APIHandler) -> None:
        self.api = api

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

        model: models.Driver = models.Driver(**driver_raw)

        model.api = self.api

        return model

    def list_drivers(self,
                     dob: Union[date, search.Search] = None,
                     email: Union[str, search.Search] = None,
                     first_name: Union[str, search.Search] = None,
                     last_name: Union[str, search.Search] = None,
                     external_id: Union[str, search.Search] = None,
                     is_active: bool = None,
                     max_records: int = None) -> Generator[models.Driver, None, None]:
        params = {}

        if dob is not None:
            params['dob'] = dob
        if email is not None:
            params['email'] = email
        if first_name is not None:
            params['firstName'] = first_name
        if last_name is not None:
            params['lastName'] = last_name
        if external_id is not None:
            params['externalId'] = external_id
        if is_active is not None:
            params['isActive'] = is_active

        count = 0
        for driver in self.api.batch_fetch("drivers",
                                            params=params):
            if max_records is not None:
                if count >= max_records:
                    break
            model: models.Driver = models.Driver(**driver)
            model.api = self.api
            yield model
            count += 1
