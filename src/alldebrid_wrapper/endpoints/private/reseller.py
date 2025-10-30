"""Reseller endpoints - voucher management."""

from typing import Literal

from ...response import APIResponse
from ..base import EndpointsBase


class ResellerEndpoints(EndpointsBase):
    """Reseller balance and voucher management endpoints."""

    def get_reseller_balance(self) -> APIResponse:
        """
        Get current reseller balance (resellers only).

        Note:
            Resellers only.
        """

        return self._make_request("GET", "/voucher/balance")

    def get_reseller_vouchers(
        self, duration: int | Literal[15, 30, 90, 180, 365], quantity: int | Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ) -> APIResponse:
        """
        Get available vouchers from reseller account (resellers only).

        Retrieves existing vouchers without generating new ones.
        May return partial list if not enough vouchers available.

        Args:
            duration: Voucher duration in days (15, 30, 90, 180, 365)
            quantity: Number of vouchers (1-10)

        Note:
            Resellers only.

        Raises:
            AllDebridAPIError: If no vouchers or invalid params
        """

        return self._make_request("POST", "/voucher/get", data={"duration": duration, "nb": quantity})

    def generate_reseller_vouchers(
        self, duration: int | Literal[15, 30, 90, 180, 365], quantity: int | Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ) -> APIResponse:
        """
        Generate new vouchers from reseller account (resellers only).

        Creates new vouchers and deducts cost from balance.

        Args:
            duration: Voucher duration in days (15, 30, 90, 180, 365)
            quantity: Number of vouchers to generate (1-10)

        Note:
            Resellers only. Cost deducted from balance.

        Raises:
            AllDebridAPIError: If insufficient balance or invalid params
        """

        return self._make_request("POST", "/voucher/generate", data={"duration": duration, "nb": quantity})
