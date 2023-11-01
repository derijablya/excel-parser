from pandas import DataFrame, Series

from app.settings import settings


async def validate_dataframe(dataframe: DataFrame):
    if len(dataframe.columns) > settings.MAX_COLS:
        raise Exception("Too many columns")
    if len(dataframe) > settings.MAX_ROWS:
        raise Exception("Too many rows")


async def validate_row(row: Series):
    if row.dropna().count() <= settings.MIN_COLS:
        raise Exception("Column has no entries")
