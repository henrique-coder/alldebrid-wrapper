from httpx import Response
from pydantic import BaseModel, ConfigDict


class APIResponse(BaseModel):
    """AllDebrid API response wrapper."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    response: Response
    data: dict | None

    @property
    def status_code(self) -> int:
        """HTTP status code."""

        return self.response.status_code

    @property
    def ok(self) -> bool:
        """Check if request was successful."""

        return self.response.is_success
