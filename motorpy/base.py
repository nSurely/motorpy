"""
motorpy base module.

This is the principal module of the motorpy project.
here you put your main classes and objects.
"""
import drivers
import vehicles
from auth import Auth

NAME = "motorpy"


class Motor(drivers.Drivers,
            vehicles.Vehicles):

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
        drivers.Drivers.__init__(self, org_id, auth, region, url)
        vehicles.Vehicles.__init__(self, org_id, auth, region, url)
