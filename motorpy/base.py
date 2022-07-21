"""
motorpy base module.

This is the principal module of the motorpy project.
here you put your main classes and objects.
"""
import motorpy.drivers as drivers
import motorpy.vehicles as vehicles
import motorpy.fleets as fleets
from motorpy.auth import Auth
from motorpy.api import APIHandler
from motorpy.api.org import OrgSettings

NAME = "motorpy"


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
                 auth: Auth,
                 region: str = None,
                 url: str = None) -> None:
        
        self.org_id = org_id
        self.auth = auth
        self.region = region
        self.url = url

        # all requests are routed through here
        # this is scoped to a single org id
        self.api = APIHandler(org_id, auth, region, url)

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
    
    def language(self):
        """Get the organization language.

        Returns:
            str: the organization language.
        """
        return self.org_settings().default_lang
    
    async def org_name(self):
        """Get the organization name.

        Returns:
            str: the organization name.
        """
        if self.api.org_data:
            return self.api.org_data.display_name
        return await self.org_settings().display_name
