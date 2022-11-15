import aiohttp
import time
from .abc import JWTAuthBase
from typing import List, Dict


class JWTAuth(JWTAuthBase):

    def __init__(self,
                 url: str,
                 org_id: str,
                 auth_type: str,
                 email: str,
                 password: str) -> None:
        self.url = url
        self.org_id = org_id

        self.auth_type = auth_type
        self.email = email
        self.password = password

        self.session = aiohttp.ClientSession()

        self.token_type: str = None
        self.access_token: str = None
        # mins
        self.expires_in: int = None
        self.refresh_token: str = None
        # mins
        self.refresh_expires_in: int = None

        # user or driver ID
        self.account_id: str = None
        # ext or int
        self.account_type: str = None

        # only used for users
        self.orgs: List[Dict[str, str]] = []

        self.last_refresh_time: float = None

        if not self.auth_type:
            raise ValueError("Auth type is required.")

        if not self.url:
            raise ValueError(
                "API handler url is required. This must be defined in the APIHandler.")

        # URL for auth actions
        # depends if user or driver profile
        self.login_url: str = None
        self.refresh_url: str = None
        self.logout_url: str = None

        if self.auth_type == "user":
            # set for users
            self.login_url = f"{self.url}/org/auth/users/login"
            self.refresh_url = f"{self.url}/org/auth/users/session/refresh"
            self.logout_url = f"{self.url}/org/auth/users/logout"
        elif self.auth_type == "driver":

            if not self.org_id:
                raise ValueError(
                    "Organization UID is required for driver auth. This must be defined in the APIHandler.")

            # set specific to drivers
            self.login_url = f"{self.url}/org/{self.org_id}/drivers/login"
            self.refresh_url = f"{self.url}/org/{self.org_id}/drivers/session/refresh"
            self.logout_url = f"{self.url}/org/{self.org_id}/drivers/logout"
        else:
            raise ValueError("Auth type must be 'user' or 'driver'.")

    def requires_refresh(self) -> bool:
        """Check if token has expired

        Returns:
            bool: True if token has expired, False otherwise.
        """
        if self.access_token is None:
            return True
        if self.expires_in is None:
            return True
        if self.last_refresh_time is None:
            return True
        # compare current time to see if minutes have passed
        if (time.time() - self.last_refresh_time) / 60 >= self.expires_in:
            return True
        return False

    async def login(self, email: str, password: str) -> str:
        """Login to the API

        Args:
            email (str): Email address of user.
            password (str): Password of user.

        Returns:
            str: the access token
        """
        token_vals = await self.session.request("POST",
                                                self.login_url,
                                                data={"email": email, "password": password}).json()
        self.token_type = token_vals["tokenType"]
        self.access_token = token_vals["accessToken"]
        self.expires_in = token_vals["expiresIn"]
        self.refresh_token = token_vals["refreshToken"]
        self.refresh_expires_in = token_vals["refreshExpiresIn"]
        self.account_id = token_vals["accountId"]
        self.account_type = token_vals["accountType"]

        if self.auth_type == 'user':
            self.orgs = token_vals["orgs"]

        self.last_refresh_time = time.time()
        return self.access_token

    async def logout(self) -> bool:
        """Logout of the API

        Returns:
            bool: True if successful, False otherwise.
        """
        if self.is_logged_in():
            await self.session.post(self.logout_url,
                                    data={"refreshToken": self.refresh_token})
            self.access_token = None
            self.expires_in = None
            self.refresh_token = None
            self.refresh_expires_in = None
            self.last_refresh_time = None
            return True
        return False

    async def refresh(self) -> None:
        """Refresh the access token

        Raises:
            ValueError: User is not logged in.
        """
        if not self.is_logged_in():
            raise ValueError("Not logged in.")

        res = await self.session.post(self.refresh_url,
                                      data={"refreshToken": self.refresh_token})
        token_vals = await res.json()
        self.token_type = token_vals["tokenType"]
        self.access_token = token_vals["accessToken"]
        self.expires_in = token_vals["expiresIn"]
        self.refresh_token = token_vals["refreshToken"]
        self.refresh_expires_in = token_vals["refreshExpiresIn"]
        self.last_refresh_time = time.time()

    def get_token(self) -> str:
        """Get the access token

        Returns:
            str: Authorization field for API requests.
        """
        return f"Bearer {self.access_token}"

    def get_headers(self) -> dict:
        """Get the headers for API requests

        Returns:
            dict: Headers for API requests.
        """
        if self.access_token is None:
            return {}
        return {"Authorization": self.get_token()}

    def is_logged_in(self) -> bool:
        """Check if user is logged in

        Returns:
            bool: True if logged in, False otherwise.
        """
        # check if token is set
        if self.access_token is None:
            return False

        # check if token has expired
        if self.requires_refresh():
            return False
        return True
