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

NAME = "motorpy"


class Motor(drivers.Drivers,
            vehicles.Vehicles,
            fleets.Fleets):

    def __init__(self,
                 org_id: str,
                 auth: Auth,
                 region: str = None,
                 url: str = None) -> None:
        """Motor Core Object. All interactions with the API are made through this object.

        Args:
            org_id (str): the UID of the organization.
            auth (Auth): the authentication object.
            region (str, optional): the region. Defaults to None.
            url (str, optional): URL override if region is not supplied. Defaults to None.
        """
        self.org_id = org_id
        self.auth = auth
        self.region = region
        self.url = url

        # all requests are routed through here
        self.api = APIHandler(org_id, auth, region, url)

        drivers.Drivers.__init__(self, self.api)
        vehicles.Vehicles.__init__(self, self.api)
        fleets.Fleets.__init__(self, self.api)

    def close(self):
        self.api.close_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
