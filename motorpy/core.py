"Core Motor Base Object - all other objects inherit from this."
from motorpy.auth import Auth
from motorpy.api import APIHandler


class MotorBase:

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
    
    def close_session(self):
        self.api.close_session()
