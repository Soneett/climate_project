from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from parsers.indicator_values import parse_indicator_values
from tables.indicator_values import IndicatorValuesTable


class IndicatorFunctionParser:
    """Adapter for indicator-specific parser functions from data/data_parsers."""

    def __init__(self, parse_function: Callable[..., dict[str, Any]], parser_name: str, source_file: str):
        self.parse_function = parse_function
        self.parser_name = parser_name
        self.source_file = source_file

    def parse(self, xlsx_path: str | Path, *, session: Session) -> dict:
        payload = self.parse_function(str(xlsx_path))

        if not isinstance(payload, dict):
            raise HTTPException(status_code=500, detail=f"{self.parser_name} must return a dict payload.")

        payload = self._normalize_payload(payload)
        rows = payload.get("indicator_values", {}).get("rows", [])
        if not isinstance(rows, list):
            raise HTTPException(status_code=500, detail=f"{self.parser_name} returned malformed rows.")

        before_count = self._count_indicator_values(session)
        parse_indicator_values(payload, session, source_file=self.source_file)
        session.commit()
        after_count = self._count_indicator_values(session)

        uploaded = max(after_count - before_count, 0)
        skipped = max(len(rows) - uploaded, 0)
        return {"uploaded": uploaded, "skipped": skipped}

    @staticmethod
    def _normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
        if "metadata" not in payload and "meta" in payload:
            payload["metadata"] = payload["meta"]
        return payload

    @staticmethod
    def _count_indicator_values(session: Session) -> int:
        count = session.query(func.count(IndicatorValuesTable.id)).scalar()
        return int(count or 0)
