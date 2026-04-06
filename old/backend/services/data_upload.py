from __future__ import annotations

import os
import tempfile
import uuid
import logging
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from parsers.indicator_values import parse_indicator_values
from tables.indicator_values import IndicatorValuesTable
from services.parsers.registry import get_parser_config, list_parser_configs


class DataUploadService:
    SUPPORTED_EXTENSIONS = {".xls", ".xlsx", ".xlsm", ".xlsb"}
    logger = logging.getLogger(__name__)

    def get_available_indicators(self) -> list[dict[str, str]]:
        return list_parser_configs()

    async def upload_file(self, session: Session, file: UploadFile, indicator_key: str) -> dict:
        filename = file.filename or ""
        extension = Path(filename).suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Use .xls, .xlsx, .xlsm or .xlsb.",
            )

        parser_config = get_parser_config(indicator_key)
        if parser_config is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown indicator_key '{indicator_key}'.",
            )

        upload_dir = Path(tempfile.gettempdir()) / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        temporary_path = upload_dir / f"{uuid.uuid4()}{extension}"

        try:
            content = await file.read()
            temporary_path.write_bytes(content)

            payload = parser_config.parse_fn(str(temporary_path))
            rows = payload.get("indicator_values", {}).get("rows", []) if isinstance(payload, dict) else []
            rows_total = len(rows)

            before_count = session.query(IndicatorValuesTable).count()
            parse_indicator_values(payload, session=session, source_file=parser_config.source_file)
            session.flush()
            after_count = session.query(IndicatorValuesTable).count()
            session.commit()

            uploaded = max(0, after_count - before_count)
            skipped = max(0, rows_total - uploaded)

            self.logger.info(
                "Data upload completed: indicator_key=%s, filename=%s, parsed_rows=%s, uploaded=%s, skipped=%s",
                indicator_key,
                filename,
                rows_total,
                uploaded,
                skipped,
            )

            return {
                "status": "success",
                "fileType": extension.lstrip("."),
                "indicator": indicator_key,
                "uploaded": uploaded,
                "skipped": skipped,
            }
        except HTTPException:
            session.rollback()
            self.logger.exception("Data upload failed with HTTPException: indicator_key=%s, filename=%s", indicator_key, filename)
            raise
        except Exception as exc:
            session.rollback()
            self.logger.exception("Data upload failed: indicator_key=%s, filename=%s", indicator_key, filename)
            raise HTTPException(status_code=500, detail=f"Failed to parse and load file: {exc}") from exc
        finally:
            if temporary_path.exists():
                os.remove(temporary_path)
