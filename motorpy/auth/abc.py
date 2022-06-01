"""
Abstract base class for any authentication method.

Note that API keys should implement just the Base class.
While JWT should implment the Base and JWTAuth classes (TBD).
"""

import abc

class AuthBase(metaclass=abc.ABCMeta):
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
    def signin(self) -> bool:
        """
        Signs in the user.
        """
        pass

    @abc.abstractmethod
    def signout(self) -> bool:
        """
        Signs out the user.
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