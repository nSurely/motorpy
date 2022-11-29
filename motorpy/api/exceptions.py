
class APIError(Exception):
    """Base class for all API exceptions"""

    def __init__(self, message: str, status_code: int = 500, url: str = None) -> None:
        # check if message implements __str__
        if not hasattr(message, "__str__"):
            message = "Unknown error - message does not implement __str__"
        
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.url = url

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message} [{self.url}]"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.status_code}, {self.message} [{self.url}])"

    @property
    def server_error(self) -> bool:
        return self.status_code >= 500

    @property
    def client_error(self) -> bool:
        return self.status_code >= 400 and self.status_code < 500

    @property
    def not_found(self) -> bool:
        return self.status_code == 404

    @property
    def bad_request(self) -> bool:
        return self.status_code == 400

    @property
    def unauthorized(self) -> bool:
        return self.status_code == 401


class APIAuthError(APIError):
    """Exception raised when the API returns an authentication error"""

    def __init__(self, message: str, status_code: int = 401, url: str = None) -> None:
        super().__init__(message, status_code, url)
