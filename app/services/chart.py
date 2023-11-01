from typing import List

from fastapi import Depends
from sqlalchemy import select
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
        if required_data.version:
            stmt = (
                select(self.version)
                .where(self.version.version == required_data.version)
                .options(
                    selectinload(self.version.project).selectinload(self.project.data)
                )
            )
        else:
            stmt = select(self.version).options(
                selectinload(self.version.project).selectinload(self.project.data)
            )

        versions = await self.repository.execute(stmt)

        date_totals = {}

        for version in versions.scalars():
            for project in version.project:
                for data_entry in project.data:
                    if (
                        required_data.year is not None
                        and data_entry.date.year != required_data.year
                    ):
                        continue

                    date_str = data_entry.date.strftime("%m/%d/%Y")

                    if date_str not in date_totals:
                        date_totals[date_str] = {
                            "date": date_str,
                            "total_plan": 0,
                            "total_fact": 0,
                        }

                    if required_data.value_type:
                        if (
                            required_data.value_type == ValueTypes.PLAN
                            and data_entry.plan
                        ):
                            date_totals[date_str]["total_plan"] += float(
                                data_entry.plan
                            )
                        elif (
                            required_data.value_type == ValueTypes.FACT
                            and data_entry.factual
                        ):
                            date_totals[date_str]["total_fact"] += float(
                                data_entry.factual
                            )
                    else:
                        if data_entry.plan:
                            date_totals[date_str]["total_plan"] += float(
                                data_entry.plan
                            )
                        if data_entry.factual:
                            date_totals[date_str]["total_fact"] += float(
                                data_entry.factual
                            )

        chart_data = list(date_totals.values())
        chart_data.sort(key=lambda x: x["date"])
        return chart_data
