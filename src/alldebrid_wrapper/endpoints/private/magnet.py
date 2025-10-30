"""Magnet and torrent management endpoints."""

from mimetypes import guess_type
from os import PathLike
from pathlib import Path
from typing import Literal

from ...exceptions import AllDebridFileNotFoundError, AllDebridInvalidFilterError, AllDebridInvalidPathError
from ...response import APIResponse
from ..base import EndpointsBase


class MagnetEndpoints(EndpointsBase):
    """Magnet/torrent upload, status, and management endpoints."""

    def upload_magnet_uris(self, magnets: list[str]) -> APIResponse:
        """
        Upload magnet URIs or info hashes to your account for processing.

        Adds torrents to your AllDebrid account using magnet links or info hashes.
        Torrents are processed server-side, and files become available for direct
        download once complete. Supports both magnet: URIs and raw info hashes.

        Supported Formats:
            - Magnet URI: magnet:?xt=urn:btih:hash&dn=name&tr=tracker...
            - Info hash (hex): abc123def456...
            - Info hash (base32): ABCDEFGH...

        Args:
            magnets: List of magnet URIs or info hashes (max 10 per request)

        Raises:
            AllDebridAPIError: If invalid or limit exceeded
        """

        return self._make_request("POST", "/magnet/upload", data={"magnets[]": magnets})

    def upload_torrent_files(self, file_paths: list[str | PathLike]) -> APIResponse:
        """
        Upload .torrent files to your account for processing.

        Adds torrents by uploading .torrent files directly instead of using magnet
        links. Useful when you have .torrent files saved locally. Files are processed
        server-side just like magnets, with the same monitoring and download workflow.

        Args:
            file_paths: List of paths to .torrent files (max 10 per request)
                       Supports absolute paths, relative paths, and tilde (~) expansion

        Note:
            Max 10/request. Same workflow as upload_magnet_uris().

        Raises:
            AllDebridFileNotFoundError: If file doesn't exist
            AllDebridInvalidPathError: If path is not a file
            AllDebridAPIError: If upload fails or invalid
        """

        files = []

        for path in file_paths:
            file_path = Path(path).expanduser().resolve()

            if not file_path.exists():
                raise AllDebridFileNotFoundError(f"Torrent file not found: {file_path.as_posix()}")

            if not file_path.is_file():
                raise AllDebridInvalidPathError(f"Path is not a file: {file_path.as_posix()}")

            mime_type = guess_type(file_path)[0]

            if mime_type:
                files.append(("files[]", (file_path.name, file_path.read_bytes(), mime_type)))
            else:
                files.append(("files[]", (file_path.name, file_path.read_bytes())))

        return self._make_request("POST", "/magnet/upload/file", files=files)

    def get_magnet_status(self, magnet_id: int) -> APIResponse:
        """
        Get detailed status and progress information for a specific magnet.

        Returns comprehensive information about a magnet's processing state,
        including download progress, upload status, file information, and
        error details if applicable. Use for monitoring individual torrents.

        Status Codes:
            0 = In Queue (waiting to start)
            1 = Downloading (actively downloading from peers)
            2 = Compressing / Moving (post-processing)
            3 = Uploading (to AllDebrid servers)
            4 = Ready (download complete, files available)
            5 = Upload failed
            6 = Internal error on unpacking
            7 = Not downloaded in 20 minutes
            8 = File too big
            9 = Internal error
            10 = Download took more than 72 hours
            11 = Deleted on hoster website
            12-13 = Processing failed
            14 = Error while contacting tracker
            15 = File not available - no peer

        Args:
            magnet_id: ID of the magnet to check (from upload response)

        Note:
            Poll every 3-5s. Use get_magnet_files() for file tree.

        Raises:
            AllDebridAPIError: If magnet_id invalid
        """

        return self._make_request("POST", "/magnet/status", data={"id": magnet_id})

    def get_all_magnets_status(
        self,
        status: list[
            str
            | Literal[
                "processing",
                "finished",
                "error",
                "queued",
                "downloading",
                "compressing",
                "uploading",
                "ready",
                "upload_failed",
                "unpacking_failed",
                "download_timeout",
                "file_too_large",
                "server_error",
                "download_expired",
                "deleted_from_hoster",
                "processing_failed",
                "tracker_unreachable",
                "no_peers_available",
            ]
        ]
        | None = None,
    ) -> APIResponse:
        """
        Get all magnets with optional client-side filtering.

        Parameters:
            status: List of status filters to apply (see below)

        Category filters (broad):
        - processing: Includes queued (0), downloading (1), compressing (2), uploading (3)
        - finished: Ready for download (4)
        - error: All error states (5-15)

        Specific filters:
        - queued (0): In Queue
        - downloading (1): Downloading
        - compressing (2): Compressing / Moving
        - uploading (3): Uploading
        - ready (4): Ready
        - upload_failed (5): Upload fail
        - unpacking_failed (6): Internal error on unpacking
        - download_timeout (7): Not downloaded in 20 min
        - file_too_large (8): File too big
        - server_error (9): Internal error
        - download_expired (10): Download took more than 72h
        - deleted_from_hoster (11): Deleted on the hoster website
        - processing_failed (12, 13): Processing failed
        - tracker_unreachable (14): Error while contacting tracker
        - no_peers_available (15): File not available - no peer
        """

        status_map = {
            "processing": [0, 1, 2, 3],
            "finished": [4],
            "error": [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            "queued": [0],
            "downloading": [1],
            "compressing": [2],
            "uploading": [3],
            "ready": [4],
            "upload_failed": [5],
            "unpacking_failed": [6],
            "download_timeout": [7],
            "file_too_large": [8],
            "server_error": [9],
            "download_expired": [10],
            "deleted_from_hoster": [11],
            "processing_failed": [12, 13],
            "tracker_unreachable": [14],
            "no_peers_available": [15],
        }

        if status:
            invalid_filters = [f for f in status if f not in status_map]

            if invalid_filters:
                raise AllDebridInvalidFilterError(
                    f"Invalid filter(s): {', '.join(invalid_filters)}. Allowed filters: {', '.join(status_map.keys())}"
                )

        response = self._make_request("POST", "/magnet/status")

        if not status or not response.data:
            return response

        magnets = response.data.get("data", {}).get("magnets", [])

        allowed_codes = []

        for f in status:
            allowed_codes.extend(status_map[f])

        allowed_codes = list(set(allowed_codes))

        filtered = [m for m in magnets if m.get("statusCode") in allowed_codes]
        response.data["data"]["magnets"] = filtered

        return response

    def get_all_magnets_incremental(self, session_id: int, counter: int) -> APIResponse:
        """
        Fetch only magnets that changed (delta sync). Saves bandwidth.

        Parameters:
            session_id: Your app ID (pick any number like 1, keep it forever)
            counter: Start with 0, then use value from previous response

        How it works:
            - counter=0 → Get ALL magnets (first time)
            - counter=N → Get ONLY changes since last call
            - API returns new counter, use it for next call

        Notes:
            - session_id is isolated per API key (no conflicts between users)
            - Lost counter? Reset with counter=0 to start fresh
            - Counter is managed by API, just pass back what it gives you
        """

        return self._make_request("POST", "/magnet/status", data={"session": session_id, "counter": counter})

    def get_magnet_files(self, magnet_ids: list[int]) -> APIResponse:
        """
        Get files and download links from one or more magnets.

        Returns the complete folder tree structure with nested files/folders
        and their download links. Use this after magnets are ready (statusCode=4).

        Structure:
            - Files at root: {"n": "file.txt", "s": 1234, "l": "https://..."}
            - Folders: {"n": "folder", "e": [...nested items...]}
            - Recursive: folders can contain files and subfolders (e = entries)

        Args:
            magnet_ids: List of magnet IDs to fetch files from
        """

        return self._make_request("POST", "/magnet/files", data={"id[]": magnet_ids})

    def delete_magnet(self, magnet_id: int) -> APIResponse:
        """
        Delete a magnet from your account.

        Permanently removes the magnet and its associated files.
        Cannot be undone.

        Args:
            magnet_id: ID of the magnet to delete

        Raises:
            AllDebridAPIError: If magnet_id invalid
        """

        return self._make_request("POST", "/magnet/delete", data={"id": magnet_id})

    def restart_magnet(self, magnet_id: int) -> APIResponse:
        """
        Restart a single failed magnet. Use for magnets with error status.

        Args:
            magnet_id: ID of the magnet to restart

        Raises:
            AllDebridAPIError: If invalid or processing/completed
        """

        return self._make_request("POST", "/magnet/restart", data={"id": magnet_id})

    def restart_magnets(self, magnet_ids: list[int]) -> APIResponse:
        """
        Restart multiple failed magnets at once. Use for magnets with error status.

        Args:
            magnet_ids: List of magnet IDs to restart

        Raises:
            AllDebridAPIError: If request fails
        """

        return self._make_request("POST", "/magnet/restart", data={"ids[]": magnet_ids})
