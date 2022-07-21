import aiohttp
from .jwt import JWTAuth
from .exceptions import DriverCreateError


class DriverAuth(JWTAuth):
    def __init__(self,
                 url: str,
                 org_id: str,
                 email: str,
                 password: str):
        super().__init__(url, org_id, "driver", email, password)

    async def signup(self,
                     email: str,
                     password: str,
                     first_name: str,
                     last_name: str,
                     fields: dict = None,
                     login: bool = True) -> dict:
        """Create a new driver profile.

        Args:
            email (str): The driver's email.
            password (str): The driver's password.
            first_name (str): The driver's first name.
            last_name (str): The driver's last name.
            fields (dict, optional): Additional API fields. Defaults to None.
            login (bool, optional): Login the driver once the account is created. Defaults to True.

        Returns:
            dict: the driver's profile
        """
        # create the driver record
        fields = fields or {}
        fields["email"] = email
        fields["password"] = password
        fields["firstName"] = first_name
        fields["lastName"] = last_name

        driver_resp = await self.session.post(
            f"/org/{self.api_handler.org_id}/drivers",
            data=fields
        )

        if driver_resp.status_code != 201:
            raise DriverCreateError(
                f"{driver_resp.status_code} - {driver_resp.text}"
            )

        # login the driver
        if login:
            await self.login(email, password)

        return driver_resp.json()
