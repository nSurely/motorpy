
class AuthError(Exception):
    """Base class for exceptions in this module."""
    pass

class APIKeyAuthError(AuthError):
    """Exception raised for errors in the APIKeyAuth class."""
    pass

class JWTAuthError(AuthError):
    """Exception raised for errors in the JWTAuth class."""
    pass

class DriverCreateError(AuthError):
    """Exception raised for errors in the DriverAuth class."""
    pass