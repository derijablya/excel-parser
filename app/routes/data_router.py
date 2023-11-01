from fastapi import APIRouter, status, Depends

from app import services
from app.serializers import ChartData

router = APIRouter(
    tags=["data"],
    prefix="/data",
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def generate_data(
    request: ChartData,
    service: services.ChartService = Depends(),
):
    return await service.generate_data(request)
