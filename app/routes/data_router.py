from typing import List

from fastapi import APIRouter, status, Depends

from app import services
from app.serializers import ChartDataIn
from app.serializers.chart_data import ChartDataOut

router = APIRouter(
    tags=["data"],
    prefix="/data",
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[ChartDataOut],
)
async def generate_data(
    request: ChartDataIn,
    service: services.ChartService = Depends(),
):
    return await service.generate_data(request)
