"""AllDebrid API configuration."""


class Config:
    """Central configuration for AllDebrid API."""

    BASE_URL: str = "https://api.alldebrid.com/{version}"
    DEFAULT_VERSION: str = "v4.1"
    FOLLOW_REDIRECTS: bool = False
    TIMEOUT: int = 15
