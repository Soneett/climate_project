from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from services.data_upload import DataUploadService

router = APIRouter(prefix="/data", tags=["Data Upload"])


@router.post("/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    indicator_key: str = Form(...),
    session: Session = Depends(get_db),
):
    service = DataUploadService()
    return await service.upload_file(session=session, file=file, indicator_key=indicator_key)


@router.get("/upload/indicators")
async def get_upload_indicators():
    service = DataUploadService()
    return service.get_available_indicators()
