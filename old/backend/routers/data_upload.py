from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from database import get_db
from services.data_upload import DataUploadService

router = APIRouter(prefix="/data", tags=["Data Upload"])


@router.post("/upload")
async def upload_data_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_db),
):
    service = DataUploadService()
    return await service.upload_file(session=session, file=file)
