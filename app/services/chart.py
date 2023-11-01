from typing import List

from fastapi import Depends
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

        data_list: List[ChartDataOut] = []

        for row in rows:
            data_dict = ChartDataOut(
                date=str(row.date),
                total_plan=float(row.total_plan) if row.total_plan else 0,
                total_fact=float(row.total_fact) if row.total_fact else 0,
            )
            data_list.append(data_dict)

        return data_list

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

        value_type_column_map = {
            "plan": self.data.plan,
            "fact": self.data.factual,
        }

        if chart_data.value_type:
            if chart_data.value_type in value_type_column_map:
                base_query = base_query.where(
                    value_type_column_map[chart_data.value_type] != None
                )

        base_query = base_query.group_by(self.data.date)

        plan_total = func.sum(self.data.plan).label("total_plan")
        fact_total = func.sum(self.data.factual).label("total_fact")

        base_query = base_query.with_only_columns(
            self.data.date, plan_total, fact_total
        )

        base_query = base_query.order_by(self.data.date)

        return base_query
