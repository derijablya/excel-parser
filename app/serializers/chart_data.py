from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.serializers.value_types import ValueTypes


class ChartDataIn(BaseModel):
    version: Optional[UUID] = None
    year: Optional[int] = None
    value_type: Optional[ValueTypes] = None


class ChartDataOut(BaseModel):
    date: str
    total_plan: float
    total_fact: float
