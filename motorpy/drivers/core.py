import motorpy.models as models
from motorpy.api import APIHandler
from datetime import date
from typing import Union, Generator
import motorpy.search as search
import asyncio


class Drivers:
    """
    Org level operations on groups of Drivers.
    """

    def __init__(self, api: APIHandler) -> None:
        self.api = api

    async def get_driver(self,
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

        driver_raw = await self.api.request(
            "GET", f"drivers/{driver_id}", params=params
        )

        model: models.Driver = models.Driver(**driver_raw)

        model.api = self.api

        return model

    async def list_drivers(self,
                           dob: Union[date, search.Search] = None,
                           email: Union[str, search.Search] = None,
                           first_name: Union[str, search.Search] = None,
                           last_name: Union[str, search.Search] = None,
                           external_id: Union[str, search.Search] = None,
                           is_active: bool = None,
                           max_records: int = None) -> Generator[models.Driver, None, None]:
        params = {}

        if dob is not None:
            params['dob'] = str(dob)
        if email is not None:
            params['email'] = str(email)
        if first_name is not None:
            params['firstName'] = str(first_name)
        if last_name is not None:
            params['lastName'] = str(last_name)
        if external_id is not None:
            params['externalId'] = str(external_id)
        if is_active is not None:
            params['isActive'] = 't' if is_active else 'f'

        count = 0
        async for driver in self.api.batch_fetch("drivers",
                                                 params=params):
            if max_records is not None:
                if count >= max_records:
                    break
            model: models.Driver = models.Driver(**driver)
            model.api = self.api
            yield model
            count += 1
            await asyncio.sleep(0.0)

    async def create_driver(self,
                            driver: models.Driver,
                            password: str = None,
                            send_invite: bool = False,
                            send_webhook: bool = True) -> models.Driver:
        """Create a new driver.
        If you would like to perform actions as this driver, you may need to login as the driver with a new motor and auth object.

        Note: the python SDK does not recommend using the JWT auth, so an API key should work fine as is.

        Args:
            driver (models.Driver): the driver model to create.
            password (str): the password for the driver, if invite is False. Defaults to None.
            send_invite (bool, optional): whether to send an invite email (password must be None if True). Defaults to False.
            send_webhook (bool, optional): whether to send a webhook. Defaults to True.

        Returns:
            models.Driver: the new driver model.
        """
        data = driver.dict(exclude_unset=True)
        if password is None and not send_invite:
            raise ValueError("You must provide a password if invite is False.")
        if password is not None and send_invite:
            raise ValueError(
                "You cannot provide a password if invite is True.")

        if password is not None:
            data['password'] = password

        driver_resp = await self.api.request(
            "POST", f"drivers", data=data, params={
                "webhook": "t" if send_webhook else "f",
                "invite": "t" if send_invite else "f"
            }
        )
        return models.Driver(**driver_resp, api=self.api)
