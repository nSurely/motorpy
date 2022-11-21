
class APIError(Exception):
    """Base class for all API exceptions"""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)

        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.status_code}, {self.message})"

    def server_error(self) -> bool:
        return self.status_code >= 500

    def client_error(self) -> bool:
        return self.status_code >= 400 and self.status_code < 500

    def not_found(self) -> bool:
        return self.status_code == 404

    def bad_request(self) -> bool:
        return self.status_code == 400

    def unauthorized(self) -> bool:
        return self.status_code == 401


class APIAuthError(APIError):
    """Exception raised when the API returns an authentication error"""

    def __init__(self, message: str, status_code: int = 401) -> None:
        super().__init__(message, status_code)
