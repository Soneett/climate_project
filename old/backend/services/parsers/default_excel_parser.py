from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session

from repo.data_upload import DataUploadRepo


class DefaultExcelParser:
    """Fallback parser that keeps compatibility with table-like indicator files."""

    def __init__(self, repo: DataUploadRepo | None = None):
        self.repo = repo or DataUploadRepo()

    def parse(self, xlsx_path: str | Path, *, session: Session) -> dict:
        extension = Path(xlsx_path).suffix.lower()
        engine = self._resolve_engine(extension)

        dataframe = pd.read_excel(xlsx_path, engine=engine)
        dataframe.columns = [str(col).strip().lower() for col in dataframe.columns]

        required = {"indicator", "region", "year", "value"}
        if not required.issubset(set(dataframe.columns)):
            raise HTTPException(
                status_code=400,
                detail="Excel must contain headers: indicator, region, year, value.",
            )

        rows_to_save: list[dict] = []
        skipped = 0

        for _, row in dataframe.iterrows():
            indicator_name = row.get("indicator")
            region_name = row.get("region")
            year = row.get("year")
            value = row.get("value")

            if pd.isna(indicator_name) or pd.isna(region_name) or pd.isna(year) or pd.isna(value):
                skipped += 1
                continue

            indicator_id = self.repo.find_indicator_id(session, str(indicator_name).strip())
            region_id = self.repo.find_region_id(session, str(region_name).strip())

            if not indicator_id or not region_id:
                skipped += 1
                continue

            source_id = None
            if "source_id" in dataframe.columns and not pd.isna(row.get("source_id")):
                source_id = int(row.get("source_id"))
            elif "source" in dataframe.columns and not pd.isna(row.get("source")):
                source_id = self.repo.find_source_id(session, str(row.get("source")).strip())

            if source_id is None:
                source_id = 1

            rows_to_save.append(
                {
                    "indicator_id": int(indicator_id),
                    "region_id": int(region_id),
                    "year": int(year),
                    "value": float(value),
                    "source_id": int(source_id),
                }
            )

        uploaded = self.repo.save_indicator_values(session=session, rows=rows_to_save) if rows_to_save else 0
        return {"uploaded": uploaded, "skipped": skipped}

    @staticmethod
    def _resolve_engine(extension: str) -> str | None:
        if extension in {".xlsx", ".xlsm"}:
            return "openpyxl"
        if extension == ".xls":
            return "xlrd"
        if extension == ".xlsb":
            return "pyxlsb"
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Use .xls, .xlsx, .xlsm or .xlsb.",
        )
