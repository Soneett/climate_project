from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from services.data_upload import DataUploadService

router = APIRouter(prefix="/data", tags=["Data Upload"])


@router.post("/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    indicator_key: str | None = Form(default=None),
    indicatorKey: str | None = Form(default=None),
    session: Session = Depends(get_db),
):
    resolved_indicator_key = indicator_key or indicatorKey
    if not resolved_indicator_key:
        raise HTTPException(status_code=422, detail="Field 'indicator_key' is required.")

    service = DataUploadService()
    return await service.upload_file(session=session, file=file, indicator_key=resolved_indicator_key)


@router.get("/upload/indicators")
async def get_upload_indicators():
    service = DataUploadService()
    return service.get_available_indicators()
