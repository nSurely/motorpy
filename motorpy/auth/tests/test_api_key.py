import pytest
from ..apikey import APIKeyAuth
from ..exceptions import APIKeyAuthError


class TestAPIKeyAuth:

    def test_init(self):
        api_key = '123'
        api_secret = '456'
        auth = APIKeyAuth(key=api_key, secret=api_secret)
        assert auth.key == api_key
        assert auth.secret == api_secret

    def test_init_no_key(self):
        with pytest.raises(APIKeyAuthError):
            APIKeyAuth(key=None, secret='456')

    def test_init_no_secret(self):
        with pytest.raises(APIKeyAuthError):
            APIKeyAuth(key='123', secret=None)

    def test_init_no_key_no_secret(self):
        with pytest.raises(APIKeyAuthError):
            APIKeyAuth(key=None, secret=None)

    def test_get_token(self):
        api_key = '123'
        api_secret = '456'
        auth = APIKeyAuth(key=api_key, secret=api_secret)
        assert auth.get_token() == f"{api_key}:{api_secret}"

    def test_get_headers(self):
        api_key = '123'
        api_secret = '456'
        auth = APIKeyAuth(key=api_key, secret=api_secret)
        assert auth.get_headers() == {
            "Authorization": f"apiKey {auth.get_token()}"
        }

    def test_requires_refresh(self):
        auth = APIKeyAuth(key='123', secret='456')
        assert not auth.requires_refresh()

    def test_refresh(self):
        auth = APIKeyAuth(key='123', secret='456')
        auth.refresh()
