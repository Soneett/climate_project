from __future__ import annotations

import inspect
import logging
import os
import tempfile
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from services.parsers.registry import get_parser


logger = logging.getLogger(__name__)


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
        parser_name = parser.__class__.__name__

        logger.info("Selected parser '%s' for indicator '%s'", parser_name, indicator_name)

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
                "parser": parser_name,
                "uploaded": uploaded,
                "skipped": skipped,
            }
        except HTTPException as exc:
            logger.exception(
                "Upload failed for indicator '%s' with parser '%s': %s",
                indicator_name,
                parser_name,
                exc.detail,
            )
            raise
        except Exception as exc:
            logger.exception(
                "Unexpected parser error for indicator '%s' with parser '%s'",
                indicator_name,
                parser_name,
            )
            raise HTTPException(
                status_code=422,
                detail=f"Failed to parse uploaded file for indicator '{indicator_name}'.",
            ) from exc
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
