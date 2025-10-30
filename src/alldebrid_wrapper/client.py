from typing import Any

from httpx import Client, HTTPError
from orjson import JSONDecodeError, loads
from pydantic import BaseModel, ConfigDict

from .config import Config
from .endpoints import Endpoints
from .endpoints.base import EndpointsBase
from .exceptions import AllDebridHTTPError, AllDebridMissingAPIKeyError
from .response import APIResponse


class AllDebridAPI(Endpoints, BaseModel):
    """Modular client for AllDebrid API."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    api_key: str | None = None

    def __init__(self, api_key: str | None = None) -> None:
        super().__init__(api_key=api_key)

        self._base_url: str = Config.BASE_URL
        self._update_client()

    def _update_client(self) -> None:
        """Update HTTP client with current API key."""

        headers = {}

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        self._client: Client = Client(headers=headers, follow_redirects=Config.FOLLOW_REDIRECTS, timeout=Config.TIMEOUT)

    def set_api_key(self, api_key: str) -> None:
        """Set or update the API key for authenticated requests.

        Args:
            api_key: AllDebrid API key for authentication
        """

        self.api_key = api_key
        self._update_client()

    def remove_api_key(self) -> None:
        """Remove the API key, allowing only public endpoint access."""

        self.api_key = None
        self._update_client()

    def close(self) -> None:
        """Close the HTTP client and release resources."""

        if hasattr(self, "_client"):
            self._client.close()

    def __enter__(self) -> "AllDebridAPI":
        """Enter context manager."""

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager and close client."""

        self.close()

    def _make_request(self, method: str, endpoint: str, version: str = Config.DEFAULT_VERSION, **kwargs: Any) -> APIResponse:
        if not EndpointsBase._is_public_endpoint(self, endpoint) and self.api_key is None:
            raise AllDebridMissingAPIKeyError(
                f"API key is required for private endpoint: {endpoint}. Use client.set_api_key('your_api_key') to set it."
            )

        url = self._base_url.format(version=version) + endpoint

        try:
            response = self._client.request(method, url, **kwargs)
        except HTTPError as e:
            raise AllDebridHTTPError(f"HTTP request error: {e}", response=None) from e

        try:
            json_data = loads(response.content)
        except JSONDecodeError:
            json_data = None

        return APIResponse(response=response, data=json_data)
