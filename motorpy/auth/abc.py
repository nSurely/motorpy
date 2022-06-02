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
        Returns True if the auth method requires a refresh.
        """
        pass

    @abc.abstractmethod
    def refresh(self) -> None:
        """
        Refreshes the auth method.
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

class JWTAuthBase(AuthBase):
    """
    Abstract base class for any JWT authentication method.
    """

    @abc.abstractmethod
    def login(self, username: str, password: str) -> str:
        """
        Login the user.
        """
        pass

    @abc.abstractmethod
    def signout(self) -> bool:
        """
        Signs out the user.
        """
        pass
    
    @abc.abstractmethod
    def signout(self) -> bool:
        """
        Signs out the user.
        """
        pass