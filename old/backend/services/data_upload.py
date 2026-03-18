from __future__ import annotations

import inspect
import os
import tempfile
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from services.parsers.registry import get_parser


class DataUploadService:
    SUPPORTED_EXTENSIONS = {".xls", ".xlsx", ".xlsm", ".xlsb"}

    async def upload_file(self, session: Session, file: UploadFile, indicator_name: str) -> dict:
        filename = file.filename or ""
        extension = Path(filename).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Use .xls, .xlsx, .xlsm or .xlsb.",
            )

        parser = get_parser(indicator_name)
        upload_dir = Path(tempfile.gettempdir()) / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        temporary_path = upload_dir / f"{uuid.uuid4()}{extension}"

        try:
            content = await file.read()
            temporary_path.write_bytes(content)

            parse_result = self._execute_parser(parser=parser, xlsx_path=temporary_path, session=session)
            uploaded = int(parse_result.get("uploaded", 0))
            skipped = int(parse_result.get("skipped", 0))

            return {
                "status": "success",
                "fileType": extension.lstrip("."),
                "indicator": indicator_name,
                "uploaded": uploaded,
                "skipped": skipped,
            }
        finally:
            if temporary_path.exists():
                os.remove(temporary_path)

    @staticmethod
    def _execute_parser(parser, xlsx_path: Path, session: Session) -> dict:
        parse_callable = getattr(parser, "parse", None)
        if not callable(parse_callable):
            raise HTTPException(status_code=500, detail="Parser does not implement parse(xlsx_path).")

        signature = inspect.signature(parse_callable)
        accepts_session = "session" in signature.parameters

        result = parse_callable(str(xlsx_path), session=session) if accepts_session else parse_callable(str(xlsx_path))

        if result is None:
            return {"uploaded": 0, "skipped": 0}

        if not isinstance(result, dict):
            raise HTTPException(status_code=500, detail="Parser must return a dict or None.")

        return result
