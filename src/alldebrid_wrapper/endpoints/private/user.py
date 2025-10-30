"""User account and management endpoints."""

from ...response import APIResponse
from ..base import EndpointsBase


class UserEndpoints(EndpointsBase):
    """User account, settings, and saved URLs endpoints."""

    def get_user(self) -> APIResponse:
        """
        Get comprehensive user account information and subscription status.

        Returns detailed information about the authenticated user including
        subscription type, premium status, remaining quotas, notifications,
        and account preferences.

        Note:
            Real-time data. Trial: 7 days or 25GB. Use clear_notification() to clear.

        Raises:
            AllDebridAPIError: If authentication fails
        """

        return self._make_request("GET", "/user")

    def get_user_supported_hosts(self) -> APIResponse:
        """
        Get user-specific list of available hosts with real-time quotas and limits.

        Returns complete list of hosts accessible to this user based on their
        subscription status (free, trial, or premium). Includes current quotas,
        remaining downloads, and concurrent download limits.

        This endpoint provides user-specific information, unlike get_supported_hosts()
        which returns global service information.

        Note:
            Real-time data. Quotas reset daily. Status updates ~10min.

        Raises:
            AllDebridAPIError: If authentication fails
        """

        return self._make_request("GET", "/user/hosts")

    def get_saved_urls(self) -> APIResponse:
        """
        Get list of URLs saved by user for later access.

        Returns all URLs that the user has explicitly saved to their account.
        These are bookmarked URLs that persist until manually deleted.
        Different from recent history which auto-expires after 3 days.

        Note:
            Persists until deleted. Different from get_recent_urls() (auto-expires).

        Raises:
            AllDebridAPIError: If authentication fails
        """

        return self._make_request("GET", "/user/links")

    def save_urls(self, urls: list[str]) -> APIResponse:
        """
        Save one or more URLs to your account for later access.

        Useful for bookmarking URLs without immediately unlocking them.

        Args:
            urls: List of URLs to save
        """

        return self._make_request("POST", "/user/links/save", data={"links[]": urls})

    def delete_saved_urls(self, urls: list[str]) -> APIResponse:
        """
        Delete one or more saved URLs from your account.

        Removes URLs from your saved list (doesn't affect unlocked URLs).

        Args:
            urls: List of URLs to delete from saved URLs
        """

        return self._make_request("POST", "/user/links/delete", data={"links[]": urls})

    def get_recent_urls(self) -> APIResponse:
        """
        Get recent download history (last 3 days).

        Returns URLs unlocked in the last 3 days. Links older than 3 days are
        automatically deleted. History logging must be enabled in account settings.

        Note:
            History logging DISABLED by default. Enable in settings.
        """

        return self._make_request("GET", "/user/history")

    def delete_recent_urls(self) -> APIResponse:
        """
        Delete all recent download history.

        Clears your entire recent links history (last 3 days).
        """

        return self._make_request("POST", "/user/history/delete")

    def check_email_verification(self, token: str) -> APIResponse:
        """
        Check email verification status for new location/device login.

        When connecting from a new location or device, AllDebrid may require
        email verification for security. This endpoint checks if the user has
        approved the new connection via email.

        Args:
            token: Verification token from AUTH_BLOCKED error response

        Raises:
            AllDebridAPIError: If token expired
        """

        return self._make_request("POST", "/user/verif", data={"token": token})

    def resend_email_verification(self, token: str) -> APIResponse:
        """
        Resend email verification for new location/device login.

        Sends the verification email again. Can only be used once per request.

        Args:
            token: Verification token from AUTH_BLOCKED error response

        Raises:
            AllDebridAPIError: If token expired or already resent
        """

        return self._make_request("POST", "/user/verif/resend", data={"token": token})

    def clear_notification(self, notification_code: str) -> APIResponse:
        """
        Clear/dismiss a specific user notification.

        Removes a notification from the user's notification list.

        Args:
            notification_code: Code of notification to clear

        Raises:
            AllDebridAPIError: If authentication fails
        """

        return self._make_request("POST", "/user/notification/clear", data={"code": notification_code})
