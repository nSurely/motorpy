import enum

from .apikey import APIKeyAuth
from .exceptions import AuthError
from .abc import AuthBase
from .driver import DriverAuth
from .user import UserAuth
from typing import Optional


# enum for auth types
class AuthType(enum.Enum):
    API_KEY = 1
    JWT_DRIVER = 2
    JWT_USER = 3


class Auth(AuthBase):

    def __init__(self,
                 api_key: str = None,
                 api_secret: str = None,
                 email: str = None,
                 password: str = None,
                 account_type: str = None) -> None:
        """Auth object for the API.
        This object can handle JWT auth and API key auth, depending on the parameters passed.

        Args:
            api_key (str, optional): API key, can be in format `pk:sk` or just `pk` (must supply secret in this case). Defaults to None.
            api_secret (str, optional): API secret key. Must be supplied if api_key not in format `pk:sk`. Defaults to None.
            email (str, optional): user/driver email. Defaults to None.
            password (str, optional): user/driver password. Defaults to None.
            account_type (str, optional): JWT account type ('user' or 'driver'). Defaults to None.

        Raises:
            AuthError: invalid credentials for either JWT (email, password, account_type) or API key auth (api_key, api_secret).
            AuthError: invalid account type for JWT auth.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.email = email
        self.password = password

        self.auth_method = None

        # this object implements the AuthBase ABC class
        self.auth_obj = None

        if self.api_key is not None:
            if self.api_secret is None:
                if ':' not in self.api_key:
                    raise AuthError('Invalid API key. API key must be in the format "key:secret".')
                splt = self.api_key.split(':')
                self.api_secret = splt[1]
                self.api_key = splt[0]
            
            self.auth_method = AuthType.API_KEY
            self.auth_obj = APIKeyAuth(
                key=self.api_key,
                secret=self.api_secret
            )
        elif self.email is not None and self.password is not None:
            if account_type == 'driver':
                self.auth_method = AuthType.JWT_DRIVER
                self.auth_obj = DriverAuth(
                    email=self.email,
                    password=self.password
                )
            elif account_type == 'user':
                self.auth_method = AuthType.JWT_USER
                self.auth_obj = UserAuth(
                    email=self.email,
                    password=self.password
                )
            else:
                raise AuthError(
                    "Invalid account type. Can only be 'driver' or 'user'.")
        else:
            raise AuthError("Auth credentials are required.")

    def requires_refresh(self) -> bool:
        return self.auth_obj.requires_refresh()

    async def refresh(self) -> None:
        await self.auth_obj.refresh()

    async def login(self) -> bool:
        if self.auth_method == AuthType.API_KEY:
            return True
        return self.auth_obj.login()

    async def logout(self) -> bool:
        if self.auth_method == AuthType.API_KEY:
            return True
        return self.auth_obj.logout()

    def get_token(self) -> str:
        return self.auth_obj.get_token()

    def get_headers(self) -> dict:
        return self.auth_obj.get_headers()

    def is_logged_in(self) -> bool:
        return self.auth_obj.is_logged_in()

    async def signup(self,
               email: str,
               password: str,
               first_name: str,
               last_name: str,
               api_fields: dict = None,
               login: bool = True) -> Optional[dict]:
        """Sign up a new user/driver.

        Args:
            email (str): account email.
            password (str): account password.
            first_name (str): account first name.
            last_name (str): account last name.
            api_fields (dict, optional): additional API fields to pass on account create. Defaults to None.
            login (bool, optional): login once created. Defaults to True.

        Returns:
            dict: the account (user/driver) object.
        """
        if self.auth_method == AuthType.API_KEY:
            return None
        return await self.auth_obj.signup(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            fields=api_fields,
            login=login
        )
