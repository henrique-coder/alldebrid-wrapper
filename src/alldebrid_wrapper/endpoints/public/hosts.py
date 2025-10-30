"""Hosts endpoints - supported hosts information."""

from ...response import APIResponse
from ..base import EndpointsBase


class HostsEndpoints(EndpointsBase):
    """Hosts information endpoints."""

    def get_supported_hosts(self) -> APIResponse:
        """
        Get comprehensive list of supported file hosts, streaming services, and redirectors.

        Returns detailed information about all services supported by AllDebrid,
        including host names, domains, URL patterns, and current status.

        Service Types:
            - Hosts: File hosting services (e.g., Mega, RapidGator, MediaFire)
            - Streams: Video streaming platforms (e.g., YouTube, Vimeo, Dailymotion)
            - Redirectors: Link shorteners/protectors (e.g., bit.ly, adf.ly, dl-protect)

        Note:
            Cache for a few hours. For user-specific limits use get_user_supported_hosts().

        Raises:
            AllDebridHTTPError: If request fails
        """

        return self._make_request("GET", "/hosts")

    def get_supported_domains(self) -> APIResponse:
        """
        Get simplified list of all supported domains organized by type.

        Returns three separate arrays of domain strings: hosts, streams, and redirectors.
        Useful for quick domain validation and lighter response payload than get_supported_hosts().

        Note:
            Cache for a few hours. Use get_supported_hosts() for detailed metadata.

        Raises:
            AllDebridHTTPError: If request fails
        """

        return self._make_request("GET", "/hosts/domains")

    def get_host_priorities(self) -> APIResponse:
        """
        Get priority ranking of file hosts from least to most restricted.

        Returns hosts ordered by their limitation level. Lower priority numbers
        indicate more open hosts with fewer restrictions, while higher numbers
        indicate hosts with more limitations (quotas, speed limits, etc.).

        Use this to choose optimal hosts when multiple options are available.

        Note:
            Global priority, not user-specific. Cache for several hours.

        Raises:
            AllDebridHTTPError: If request fails
        """

        return self._make_request("GET", "/hosts/priority")
