"""Base class for all endpoints with shared request method."""

from typing import Any

from ..config import Config
from ..response import APIResponse


class EndpointsBase:
    """Base class containing the _make_request method."""

    # Public endpoints that don't require API key
    PUBLIC_ENDPOINTS = {"/ping", "/hosts", "/hosts/domains", "/hosts/priority"}

    def _is_public_endpoint(self, endpoint: str) -> bool:
        """Check if endpoint is public and doesn't require API key."""

        return endpoint in self.PUBLIC_ENDPOINTS

    def _make_request(self, method: str, endpoint: str, version: str = Config.DEFAULT_VERSION, **kwargs: Any) -> APIResponse:
        """Make HTTP request to AllDebrid API."""

        ...
