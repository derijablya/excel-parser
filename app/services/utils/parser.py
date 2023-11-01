from typing import Dict

import pandas as pd
from fastapi import File

from app.services.utils.validator import validate_row, validate_dataframe


async def parse_data(file: File) -> Dict:
    dataframe = pd.read_excel(
        file,
    ).replace({pd.NA: None})
    await validate_dataframe(dataframe)
    date_columns = dataframe.columns[2::2]
    data = dataframe.iloc[1:]
    result = {}
    for index, row in data.iterrows():
        await validate_row(row)
        project_key = (row["Unnamed: 0"], row["Unnamed: 1"])
        project_values = []

        plan_values = row[2::2]
        fact_values = row[3::2]

        for date, plan_val, fact_val in zip(date_columns, plan_values, fact_values):
            date = date.date()
            project_values.append(
                {"date": date, "plan_val": plan_val, "fact_val": fact_val}
            )
        result[project_key] = project_values
    return result
