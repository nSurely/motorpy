from .jwt import JWTAuth
from .exceptions import AuthError


class UserAuth(JWTAuth):

    def __init__(self,
                 url: str,
                 org_id: str,
                 email: str,
                 password: str):
        super().__init__(url, org_id, "user", email, password)

    async def signup(self,
               email: str,
               password: str,
               first_name: str,
               last_name: str,
               fields: dict = None,
               login: bool = True) -> dict:
        """Will throw an error
        """
        raise AuthError(
            "UserAuth.signup() is not implemented. A user must be added by another authenticated user.")
