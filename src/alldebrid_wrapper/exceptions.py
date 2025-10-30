from httpx import Response


class AllDebridAPIError(Exception):
    """Base exception for AllDebrid API errors."""

    def __init__(self, message: str, response: Response | None = None, json_data: dict | None = None) -> None:
        self.message = message
        self.response = response
        self.json_data = json_data

        super().__init__(self.message)


class AllDebridHTTPError(AllDebridAPIError):
    """Exception raised for HTTP request errors."""

    pass


class AllDebridFileNotFoundError(AllDebridAPIError):
    """Exception raised when a torrent file is not found."""

    pass


class AllDebridInvalidPathError(AllDebridAPIError):
    """Exception raised when a path is not a valid file."""

    pass


class AllDebridInvalidFilterError(AllDebridAPIError):
    """Exception raised when an invalid filter is provided."""

    pass


class AllDebridMissingAPIKeyError(AllDebridAPIError):
    """Exception raised when API key is required but not provided."""

    pass
