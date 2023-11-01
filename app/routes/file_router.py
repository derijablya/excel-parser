import tempfile
import uuid

from fastapi import APIRouter, status, UploadFile, Depends, HTTPException
from starlette.responses import FileResponse

from app import services
from app.serializers import Version

router = APIRouter(
    tags=["File"],
    prefix="/file",
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Version,
)
async def create_upload_file(
    file: UploadFile,
    service: services.ExcelService = Depends(),
):
    return await service.load_excel_file(file.file)


@router.get(
    "/{version}",
    status_code=status.HTTP_200_OK,
)
async def get_upload_file(
    version: uuid.UUID,
    service: services.ExcelService = Depends(),
):
    excel_data = await service.get_excel_file(version)
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_filename = tmp_file.name
        tmp_file.write(excel_data.getvalue())
        return FileResponse(tmp_filename, filename=f"{version}.xlsx")
