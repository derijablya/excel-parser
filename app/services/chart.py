from typing import List

from fastapi import Depends
from pydantic import TypeAdapter
from sqlalchemy import select, extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import models
from app.repository.postgres import get_session
from app.serializers import ChartDataIn
from app.serializers import ChartDataOut, ValueTypes


class ChartService:
    def __init__(self, repository: AsyncSession = Depends(get_session)):
        self.repository = repository
        self.project = models.Project
        self.data = models.Data
        self.version = models.Version

    async def generate_data(self, required_data: ChartDataIn) -> List[ChartDataOut]:
        query = await self.build_query(required_data)
        result = await self.repository.execute(query)
        rows = result.fetchall()
        return TypeAdapter(List[ChartDataOut]).validate_python(rows)

    async def build_query(self, chart_data: ChartDataIn):
        base_query = (
            select(self.version, self.data)
            .join_from(self.version, self.project)
            .join_from(self.project, self.data)
        )

        if chart_data.version:
            base_query = base_query.where(self.version.version == chart_data.version)

        if chart_data.year:
            base_query = base_query.where(
                extract("year", self.data.date) == chart_data.year
            )

        base_query = base_query.group_by(self.data.date)

        plan_total = func.sum(self.data.plan).label("total_plan")
        fact_total = func.sum(self.data.factual).label("total_fact")

        if chart_data.value_type == ValueTypes.PLAN:
            base_query = base_query.add_columns(plan_total)
            base_query = base_query.with_only_columns(self.data.date, plan_total)
        elif chart_data.value_type == ValueTypes.FACT:
            base_query = base_query.add_columns(fact_total)
            base_query = base_query.with_only_columns(self.data.date, fact_total)
        else:
            base_query = base_query.add_columns(plan_total, fact_total)
            base_query = base_query.with_only_columns(
                self.data.date, plan_total, fact_total
            )

        base_query = base_query.order_by(self.data.date)

        return base_query
