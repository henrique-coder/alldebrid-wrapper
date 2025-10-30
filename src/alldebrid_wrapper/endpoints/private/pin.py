"""PIN authentication endpoints."""

from ...response import APIResponse
from ..base import EndpointsBase


class PinEndpoints(EndpointsBase):
    """PIN-based authentication endpoints."""

    def get_pin_code(self) -> APIResponse:
        """
        Generate PIN code for user authentication flow.

        Creates a temporary PIN code that users enter on AllDebrid website
        to authorize your application. This is the first step in PIN-based
        authentication, which allows users to authenticate without sharing
        their API key directly.

        PIN Authentication Flow:
            1. Call get_pin_code() to generate PIN and check token
            2. Display PIN to user (show user_url or base_url)
            3. User visits AllDebrid website and enters PIN
            4. Poll check_pin_status() until user completes authentication
            5. Retrieve API key from successful check response

        Note:
            Resellers only.

        Raises:
            AllDebridHTTPError: If request fails
        """

        return self._make_request("GET", "/pin/get")

    def check_pin_status(self, check_token: str, pin: str) -> APIResponse:
        """
        Check PIN authentication status and retrieve API key when ready.

        Polls the PIN verification endpoint to check if user has submitted
        the PIN code on AllDebrid website. Returns API key once user completes
        authentication. This is step 2 of the PIN authentication flow.

        Args:
            check_token: Check token from get_pin_code() response
            pin: PIN code from get_pin_code() response

        Note:
            Poll every 5+ seconds. Expires after 10 minutes.

        Raises:
            AllDebridAPIError: If PIN expired or invalid
        """

        return self._make_request("POST", "/pin/check", data={"check": check_token, "pin": pin})
