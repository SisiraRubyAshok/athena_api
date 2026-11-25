from typing import Any

from pydantic import BaseModel


class VehicleResponse(BaseModel):
    data: dict[str, Any]