from .abc import AuthBase
from .exceptions import APIKeyAuthError


class APIKeyAuth(AuthBase):

    def __init__(self, key: str, secret: str) -> None:
        self.key = key
        self.secret = secret
        self.headers: dict = None

        if not self.key:
            raise APIKeyAuthError("API key is required.")

        if not self.secret:
            raise APIKeyAuthError("API secret is required.")
        
        self.secret = self.secret.strip()
        self.key = self.key.strip()

    def requires_refresh(self) -> bool:
        return False

    async def refresh(self) -> None:
        pass

    def get_token(self) -> str:
        return f"{self.key}:{self.secret}"

    def get_headers(self) -> dict:
        if self.headers is None:
            self.headers = {
                "Authorization": f"apiKey {self.get_token()}"
            }
        return self.headers
    
    def is_logged_in(self) -> bool:
        return True
