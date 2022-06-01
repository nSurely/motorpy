import requests
from auth import Auth

from .exceptions import APIError
from typing import Generator


class APIHandler:

    def __init__(self,
                 org_id: str,
                 auth: Auth,
                 region: str = None,
                 url: str = None,
                 timeout: float = 10.0) -> None:
        """
        APIHandler makes requests to the API and handles authentication.

        Args:
            org_id (str): the UID of the organization.
            auth (Auth): the authentication object.
            region (str, optional): the region. Defaults to None.
            url (str, optional): URL override if region is not supplied. Defaults to None.

        Raises:
            ValueError: URL or Region is not supplied.
            ValueError: Invalid region.
        """
        self.org_id = org_id
        self.auth = auth
        self.region = region
        self.url = url
        self.timeout = timeout

        if not self.region and not self.url:
            raise ValueError("Region or URL must be specified.")

        if self.url:
            self.url = self.url.rstrip("/")

            if self.url.endswith('/'):
                self.url = self.url[:-1]
        else:
            if region not in {"eu-1", "us-1", "me-1"}:
                raise ValueError("Region must be one of: eu-1, us-1, me-1")
            self.url = f"https://{self.region}.nsurely-motor.com/v1/api"

        self.org_url = f"{self.url}/org/{self.org_id}"

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        if self.auth.requires_refresh():
            self.auth.refresh()

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'] = self.auth.get_headers()
        kwargs['headers'].update(kwargs.pop("headers", {}))

        return requests.request(method, url, **kwargs, headers=kwargs['headers'], timeout=self.timeout)

    def request(self,
                method: str,
                endpoint: str,
                params: dict = None,
                data: dict = None,
                headers: dict = None) -> dict:
        """Make a request to the API.

        Args:
            method (str): the HTTP method.
            endpoint (str): URL path to the API endpoint.
            params (dict, optional): query params. Defaults to None.
            data (dict, optional): body. Defaults to None.
            headers (dict, optional): headers. Defaults to None.

        Raises:
            APIError: an API error occurred.

        Returns:
            Optional[dict]: response body if supplied.
        """
        res = self._make_request(
            method, f"{self.org_url}/{endpoint}", params=params, data=data, headers=headers)

        if res.status_code == 401:
            self.auth.refresh()
            headers.update(self.auth.get_headers())
            res = self._make_request(
                method, f"{self.org_url}/{endpoint}", params=params, data=data, headers=headers)

        if res.status_code < 300:
            return res.json() if res.json() else None
        else:
            raise APIError(f"{res.status_code} - {res.text}")

    def batch_fetch(self,
                    endpoint: str,
                    params: dict = None,
                    headers: dict = None,
                    limit: int = 50,
                    offset: int = 0) -> Generator[dict, None, None]:
        """Fetch a batch of data from the API."""
        while True:
            res = self.request(
                "GET",
                endpoint,
                params=params,
                headers=headers
            )

            if res:
                for item in res:
                    yield item

                if len(res) < limit:
                    break

                offset += limit
                params['offset'] = offset
            else:
                break
