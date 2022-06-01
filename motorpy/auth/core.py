import enum

from .apikey import APIKeyAuth
from .exceptions import AuthError
from .abc import AuthBase


# enum for auth types
class AuthType(enum.Enum):
    API_KEY = 1
    JWT = 2


class Auth(AuthBase):

    def __init__(self,
                 api_key: str = None,
                 api_secret: str = None,
                 username: str = None,
                 password: str = None) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.username = username
        self.password = password

        self.auth_method = None

        # this object implements the AuthBase ABC class
        self.auth_obj = None

        if self.api_key is not None and self.api_secret is not None:
            self.auth_method = AuthType.API_KEY
            self.auth_obj = APIKeyAuth(
                key=self.api_key,
                secret=self.api_secret
            )
        elif self.username is not None and self.password is not None:
            self.auth_method = AuthType.JWT

            raise AuthError("JWT auth not yet implemented.")
        else:
            raise AuthError("Auth credentials are required.")

    def requires_refresh(self) -> bool:
        return self.auth_obj.requires_refresh()

    def refresh(self) -> None:
        self.auth_obj.refresh()

    def signin(self) -> bool:
        return self.auth_obj.signin()

    def signout(self) -> bool:
        return self.auth_obj.signout()

    def get_token(self) -> str:
        return self.auth_obj.get_token()

    def get_headers(self) -> dict:
        return self.auth_obj.get_headers()
