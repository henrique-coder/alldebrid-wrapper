"""Ping endpoint - check API availability."""

from ...response import APIResponse
from ..base import EndpointsBase


class PingEndpoints(EndpointsBase):
    """Ping endpoint."""

    def ping(self) -> APIResponse:
        """
        Check AllDebrid API availability and responsiveness.

        Use this endpoint to verify that the API is operational and
        reachable from your network. Returns a simple pong response.

        Raises:
            AllDebridHTTPError: If API is unreachable
        """

        return self._make_request("GET", "/ping")
