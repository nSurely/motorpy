"""
motorpy base module.

This is the principal module of the motorpy project.
here you put your main classes and objects.
"""
import asyncio
import sys
from typing import Union
import motorpy.drivers as drivers
import motorpy.vehicles as vehicles
import motorpy.fleets as fleets
from motorpy.auth import Auth
from motorpy.api import APIHandler
from motorpy.api.core import APIHandlerNoAuth
from motorpy.api.org import OrgSettings

NAME = "motorpy"

# known event loop issue
# https://github.com/encode/httpx/issues/914
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Motor(drivers.Drivers,
            vehicles.Vehicles,
            fleets.Fleets):
    """Motor Core Object. All interactions with the API are made through this object.

    Args:
        org_id (str): the UID of the organization.
        auth (Auth): the authentication object.
        region (str, optional): the region. Defaults to None.
        url (str, optional): URL override if region is not supplied. Defaults to None.
    """

    def __init__(self,
                 org_id: str,
                 auth: Auth = None,
                 region: str = None,
                 url: str = None) -> None:

        self.org_id = org_id
        self.auth = auth
        self.region = region
        self.url = url

        # all requests are routed through here
        # this is scoped to a single org id
        if self.auth is not None:
            self.api = APIHandler(org_id, auth, region, url)
        else:
            self.api = APIHandlerNoAuth(org_id, region, url)

        drivers.Drivers.__init__(self, self.api)
        vehicles.Vehicles.__init__(self, self.api)
        fleets.Fleets.__init__(self, self.api)

    async def close(self):
        await self.api.close_session()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def org_settings(self) -> 'OrgSettings':
        """Get the organization settings.

        Returns:
            OrgSettings: the organization settings.
        """
        if not self.api.org_data:
            await self.api.refresh_org_data()
        return self.api.org_data

    async def language(self):
        """Get the organization language.

        Returns:
            str: the organization language.
        """
        if self.api.org_data:
            return self.api.org_data.default_lang
        return await self.org_settings().default_lang

    async def org_name(self):
        """Get the organization name.

        Returns:
            str: the organization name.
        """
        if self.api.org_data:
            return self.api.org_data.display_name
        return await self.org_settings().display_name

    async def request(self,
                      method: str,
                      path: str,
                      data: Union[dict, list] = None,
                      params: dict = None,
                      headers: dict = None) -> Union[dict, list]:
        """Make a request to the API.

        Args:
            method (str): the HTTP method.
            path (str): the path. The path is relative to the API base URL and org id, ie. <base url>/org/<org_id>/<<your path>>
            data (Union[dict, list]): the data.
            params (dict): the query string.
            headers (dict): the headers.

        Returns:
            Union[dict, list]: the API body response.
        """
        if not path.startswith("/"):
            path = f"/{path}"
        return await self.api.request(
            method=method,
            endpoint=path,
            data=data,
            params=params,
            headers=headers
        )
