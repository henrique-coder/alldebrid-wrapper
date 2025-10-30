"""Private endpoints - require authentication."""

from .magnet import MagnetEndpoints
from .pin import PinEndpoints
from .reseller import ResellerEndpoints
from .url import UrlEndpoints
from .user import UserEndpoints


__all__ = ["MagnetEndpoints", "PinEndpoints", "ResellerEndpoints", "UrlEndpoints", "UserEndpoints"]
