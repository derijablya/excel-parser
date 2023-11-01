from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ChartData(BaseModel):
    version: Optional[UUID] = None
    year: Optional[int] = None
    value_type: Optional[str] = None
