"""
Abstract base classes for any authentication methods.

Note that API keys should implement just the Base class.
While JWT should implment the Base and JWTAuth classes (TBD).
"""

import abc


class AuthBase(metaclass=abc.ABCMeta):
    """
    Abstract base class for any authentication method.
    """

    # putting refresh in base ABC class here so that it can be used by all auth methods
    # this doesn't apply to API key auth so simply return False
    # doing this as refresh is called frequently in many places, and this avoids checking the type of auth
    @abc.abstractmethod
    def requires_refresh(self) -> bool:
        """
        Returns True if the auth token requires a refresh.
        """
        pass

    @abc.abstractmethod
    async def refresh(self) -> None:
        """
        Refreshes the auth token.
        """
        pass

    @abc.abstractmethod
    def get_token(self) -> str:
        """
        Returns the current token.
        """
        pass

    @abc.abstractmethod
    def get_headers(self) -> dict:
        """
        Returns the current headers.
        """
        pass

    @abc.abstractmethod
    def is_logged_in(self) -> bool:
        """
        Returns True if the auth token is valid. True always for API Key.
        """
        pass


class JWTAuthBase(AuthBase):
    """
    Abstract base class for any JWT authentication method.
    """
    @abc.abstractmethod
    async def login(self, email: str, password: str) -> str:
        """
        Login the user/driver.
        """
        pass

    @abc.abstractmethod
    async def logout(self) -> bool:
        """
        Signs out the user/driver.
        """
        pass

    @abc.abstractmethod
    async def signup(self,
               email: str,
               password: str,
               first_name: str,
               last_name: str,
               fields: dict = None,
               login: bool = True) -> dict:
        """
        Signup the user/driver.
        Returns the user/driver's profile.
        """
        pass


class JWTDriverAuthBase(JWTAuthBase):
    """
    Abstract base class for any JWT authentication method for drivers.
    """
    pass


class JWTUserAuthBase(JWTAuthBase):
    """
    Abstract base class for any JWT authentication method for users.
    """

    pass
