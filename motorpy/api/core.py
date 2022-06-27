import aiohttp
import requests
import os
import asyncio
from motorpy.auth import Auth

from .exceptions import APIError
from typing import Generator, List, Optional, Coroutine, Tuple


def _make_request(method: str, url: str,
                  params: dict = None,
                  data: dict = None,
                  headers: dict = None,
                  timeout=10.0) -> Tuple[Optional[dict], int]:
    """
    Make synchronous request to the API
    """
    res = requests.request(method, url, headers=headers,
                           params=params, data=data, timeout=timeout)
    return res.json() if res.json() else None, res.status_code


async def _async_request(session: aiohttp.ClientSession,
                         method: str,
                         url: str,
                         params: dict = None,
                         data: dict = None,
                         headers: dict = None,
                         timeout=10.0) -> Tuple[Optional[dict], int]:
    """
    Make asynchronous request to the API.
    """
    async with session.request(method, url, params=params, data=data, headers=headers, timeout=timeout) as res:
        return await res.json() if await res.json() else None, res.status


class APIHandlerNoAuth:

    def __init__(self,
                 org_id: str,
                 region: str = None,
                 url: str = None,
                 timeout: float = 10.0,
                 async_requests: bool = False) -> None:
        self.org_id = org_id
        self.region = region
        self.url = url
        self.timeout = timeout
        self.async_requests = async_requests

        # async session to be used if async_requests is True
        self.session = aiohttp.ClientSession() if async_requests else None

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

        self.telematics_url = f"https://{self.region}.nsurely-motor.com/v1/telematics"

        self.org_url = f"{self.url}/org/{self.org_id}"

    def _loop_request(self,
                      method: str,
                      url: str,
                      params: dict = None,
                      data: dict = None,
                      headers: dict = None) -> Tuple[Optional[dict], int]:
        if not self.async_requests:
            body, status = _make_request(
                method,
                url,
                params=params,
                data=data,
                headers=headers,
                timeout=self.timeout)
        else:
            body, status = asyncio.run(_async_request(self.session,
                                                      method,
                                                      url,
                                                      params=params,
                                                      data=data,
                                                      headers=headers,
                                                      timeout=self.timeout))
        return body, status

    def request(self,
                method: str,
                endpoint: str,
                params: dict = None,
                data: dict = None,
                headers: dict = None) -> Optional[dict]:
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
        body, status = self._loop_request(
            method, f"{self.org_url}/{endpoint}",
            params=params,
            data=data,
            headers=headers)

        if status < 300:
            return body
        else:
            raise APIError(f"API responded with {status}")

    def close_session(self) -> None:
        """Close the asynchronous session."""
        if self.async_requests:
            self.session.close()

    def __del__(self) -> None:
        # ! this is only called when ref count is 0
        # so in practice this wont be called but just in case
        # better to use context manager!
        self.close_session()


class APIHandler(APIHandlerNoAuth):

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

        super().__init__(org_id, region, url, timeout)

    def _make_request(self, method: str, url: str, **kwargs) -> Tuple[Optional[dict], int]:
        if self.auth.requires_refresh():
            self.auth.refresh()

        if 'headers' not in kwargs:
            kwargs['headers'] = {}

        kwargs['headers'] = {
            **kwargs['headers'],
            **self.auth.get_headers()
        }

        return self._loop_request(method,
                                  url,
                                  headers=kwargs['headers'],
                                  params=kwargs.get('params', {}))

    def auth_ok(self) -> bool:
        """Check if the auth token is still valid."""
        if not self.auth.is_logged_in():
            return False
        if self.auth.requires_refresh():
            return False
        return True

    def check_auth(self) -> None:
        if not self.auth_ok():
            if not self.auth.is_logged_in():
                self.auth.login()
                return
            if self.auth.requires_refresh():
                self.auth.refresh()

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
        headers = headers or {}
        params = params or {}

        self.check_auth()

        body, status = self._make_request(
            method, f"{self.org_url}/{endpoint}", params=params, data=data, headers=headers)

        if status == 401:
            self.check_auth()
            headers.update(self.auth.get_headers())
            body, status = self._make_request(
                method, f"{self.org_url}/{endpoint}", params=params, data=data, headers=headers)

        if status < 300:
            return body
        else:
            raise APIError(f"API responded with {status} - {body}")

    def download_file(self, url: str, file_location: str, save_dir: str = None) -> str:
        """Downloads a file to local disk.

        Args:
            url (str): the record URL (eg. driver URL).
            file_location (str): the file location.
            save_dir (str, optional): the directory to save the file to. Defaults to None.

        Returns:
            str: the file location
        """
        self.check_auth()

        local_filename = file_location.split('/')[-1]
        if save_dir is None:
            save_loc = os.path.join(os.getcwd(), local_filename)
        else:
            save_loc = os.path.abspath(save_dir)
            save_loc = os.path.join(save_loc, local_filename)

        with requests.get(os.path.join(url, file_location), headers=self.auth.get_headers(), stream=True) as r:
            r.raise_for_status()
            with open(save_loc, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return save_loc

    def telematics_request(self,
                           method: str,
                           endpoint: str,
                           params: dict = None,
                           data: dict = None,
                           headers: dict = None) -> Optional[dict]:
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
        body, status = self._loop_request(
            method, f"{self.telematics_url}/{endpoint}", params=params, data=data, headers=headers)

        if status < 300:
            return body
        else:
            raise APIError(f"API responded with {status}")

    def batch_fetch(self,
                    endpoint: str,
                    params: dict = None,
                    headers: dict = None,
                    limit: int = 50,
                    offset: int = 0) -> Generator[List[dict], None, None]:
        """Fetch a batch of data from the API."""
        params = params or {}
        headers = headers or {}

        params['limit'] = limit
        params['offset'] = offset

        while True:
            body = self.request(
                "GET",
                endpoint,
                params=params,
                headers=headers
            )

            if body:
                yield from body

                if len(body) < limit:
                    break

                offset += limit
                params['offset'] = offset
            else:
                # yield empty list
                yield from []
                break
