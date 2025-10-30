"""URL unlock and link management endpoints."""

from ...response import APIResponse
from ..base import EndpointsBase


class UrlEndpoints(EndpointsBase):
    """URL info, unlock, and redirector endpoints."""

    def get_url_info(self, urls: list[str], password: str | None = None) -> APIResponse:
        """
        Get detailed information about URLs without unlocking them.

        Retrieves file metadata from host servers including filename, size,
        and host information. Useful for validating URLs and previewing content
        before unlocking. Does not consume download quotas.

        Args:
            urls: List of URLs to check (max 10 URLs per request)
            password: Password for protected archives (optional)

        Note:
            No quota consumed.

        Raises:
            AllDebridAPIError: If URLs invalid
        """

        data = {"link[]": urls}

        if password:
            data["password"] = password

        return self._make_request("POST", "/link/infos", data=data)

    def extract_redirector_urls(self, url: str) -> APIResponse:
        """
        Extract real URLs from link shorteners and redirectors.

        Unwraps URLs hidden behind redirector services like bit.ly, adf.ly,
        dl-protect.link, and other link shorteners. Automatically follows
        redirect chains to reveal the final destination URLs.

        Supported redirectors include:
            - Link shorteners: bit.ly, tinyurl, goo.gl, etc.
            - Link protectors: dl-protect.link, linkvertise, etc.
            - Ad-link services: adf.ly, bc.vc, etc.

        Args:
            url: Redirector/shortener URL to extract from

        Note:
            Follows redirect chains. May return multiple URLs.

        Raises:
            AllDebridAPIError: If redirector not supported
        """

        return self._make_request("POST", "/link/redirector", data={"link": url}, follow_redirects=True)

    def unlock_url(self, url: str, password: str | None = None) -> APIResponse:
        """
        Unlock a URL and get direct download link.

        Converts premium host URLs into direct, high-speed download links.
        This is the primary method for downloading files from supported hosts.
        Consumes download quotas for limited hosts.

        Response Types:
            - Instant unlock: Direct download link returned immediately
            - Delayed unlock: Returns delayed ID (use check_delayed_url)
            - Stream selection: Returns streams array (use select_stream_quality)

        Args:
            url: Premium host URL to unlock
            password: Password for protected archives (optional)

        Note:
            Links expire after ~4h inactivity. Check quotas before unlocking.

        Raises:
            AllDebridAPIError: If invalid, unsupported, or quota exceeded
        """

        data = {"link": url}

        if password:
            data["password"] = password

        return self._make_request("POST", "/link/unlock", data=data)

    def select_stream_quality(self, generation_id: str, stream_id: str) -> APIResponse:
        """
        Select stream quality and get direct download link for video streams.

        After unlocking a streaming URL (YouTube, Vimeo, etc.) that returns
        multiple quality options, use this method to select desired quality
        and receive the direct download link.

        Workflow:
            1. Call unlock_url() with streaming service URL
            2. Response contains streams array with quality options
            3. Call select_stream_quality() with chosen stream ID
            4. Receive direct download link for selected quality

        Args:
            generation_id: Generation ID from unlock_url() response (data.id)
            stream_id: Stream ID of chosen quality (from streams array)

        Note:
            Use generation ID promptly before expiration.

        Raises:
            AllDebridAPIError: If generation_id expired or stream_id invalid
        """

        return self._make_request("POST", "/link/streaming", data={"id": generation_id, "stream": stream_id})

    def check_delayed_url(self, delayed_id: int) -> APIResponse:
        """
        Check status and retrieve download link for delayed unlock operations.

        Some hosts require processing time before download links are ready.
        When unlock_url() returns a delayed ID instead of immediate link,
        use this method to poll for completion and retrieve the final link.

        Polling Strategy:
            - Poll every 2-3 seconds for responsive user experience
            - Timeout after 60 seconds (most unlocks complete within 30s)
            - Check for error status codes to stop early

        Args:
            delayed_id: Delayed ID from unlock_url() response (data.delayed)

        Note:
            Most complete in 10-30s. Poll every 2-3s.

        Raises:
            AllDebridAPIError: If delayed_id invalid or expired
        """

        return self._make_request("POST", "/link/delayed", data={"id": delayed_id})
