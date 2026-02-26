from sqlalchemy.orm import Session

from tables.indicators import IndicatorsTable
from tables.indicator_values import IndicatorValuesTable
from tables.regions import RegionsTable


class AnalyticsRepo:
    def get_region(self, session: Session, region_id: int) -> RegionsTable | None:
        return (
            session.query(RegionsTable)
            .filter(RegionsTable.id == region_id, RegionsTable.is_deleted == False)
            .one_or_none()
        )

    def get_indicators(
        self,
        session: Session,
        indicator_ids: list[int],
    ) -> list[IndicatorsTable]:
        if not indicator_ids:
            return []

        return (
            session.query(IndicatorsTable)
            .filter(IndicatorsTable.id.in_(indicator_ids), IndicatorsTable.is_deleted == False)
            .all()
        )

    def get_indicator_values(
        self,
        session: Session,
        region_id: int,
        indicator_ids: list[int],
    ) -> list[IndicatorValuesTable]:
        if not indicator_ids:
            return []

        return (
            session.query(IndicatorValuesTable)
            .filter(
                IndicatorValuesTable.region_id == region_id,
                IndicatorValuesTable.indicator_id.in_(indicator_ids),
                IndicatorValuesTable.is_deleted == False,
            )
            .order_by(IndicatorValuesTable.year.asc())
            .all()
        )