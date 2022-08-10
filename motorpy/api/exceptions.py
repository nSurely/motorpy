
class APIError(Exception):
    """Base class for all API exceptions"""
    pass

class APIAuthError(APIError):
    """Exception raised when the API returns an authentication error"""
    pass