"""Main Endpoints class that combines all endpoint categories."""

from .private import MagnetEndpoints, PinEndpoints, ResellerEndpoints, UrlEndpoints, UserEndpoints
from .public import HostsEndpoints, PingEndpoints


class Endpoints(
    PingEndpoints,
    HostsEndpoints,
    PinEndpoints,
    UserEndpoints,
    UrlEndpoints,
    MagnetEndpoints,
    ResellerEndpoints,
):
    """All AllDebrid API endpoints combined."""

    pass
