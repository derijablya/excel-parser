import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.serializers.value_types import ValueTypes


class ChartDataIn(BaseModel):
    version: Optional[UUID] = None
    year: Optional[int] = None
    value_type: Optional[ValueTypes] = None


class ChartDataOut(BaseModel):
    date: datetime.date
    total_plan: Optional[float] = None
    total_fact: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
