from sqlalchemy import func
from sqlalchemy.orm import Session

from tables.data_sources import DataSourcesTable
from tables.indicators import IndicatorsTable
from tables.indicator_values import IndicatorValuesTable
from tables.regions import RegionsTable


class DataUploadRepo:
    def find_indicator_id(self, session: Session, indicator: str) -> int | None:
        row = (
            session.query(IndicatorsTable)
            .filter(
                func.lower(IndicatorsTable.name) == indicator.lower(),
                IndicatorsTable.is_deleted == False,
            )
            .first()
        )
        return row.id if row else None

    def find_region_id(self, session: Session, region: str) -> int | None:
        row = (
            session.query(RegionsTable)
            .filter(
                func.lower(RegionsTable.name) == region.lower(),
                RegionsTable.is_deleted == False,
            )
            .first()
        )
        return row.id if row else None

    def find_source_id(self, session: Session, source: str) -> int | None:
        row = (
            session.query(DataSourcesTable)
            .filter(
                func.lower(DataSourcesTable.name) == source.lower(),
                DataSourcesTable.is_deleted == False,
            )
            .first()
        )
        return row.id if row else None

    def save_indicator_values(self, session: Session, rows: list[dict]) -> int:
        records = [IndicatorValuesTable(**row) for row in rows]
        session.bulk_save_objects(records)
        session.commit()
        return len(records)
