from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from services.data_upload import DataUploadService

router = APIRouter(prefix="/data", tags=["Data Upload"])


@router.post("/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    indicator_name: str = Form(...),
    session: Session = Depends(get_db),
):
    service = DataUploadService()
    return await service.upload_file(session=session, file=file, indicator_name=indicator_name)
