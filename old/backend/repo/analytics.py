from sqlalchemy import func
from sqlalchemy.orm import Session

from tables.indicators import IndicatorsTable
from tables.indicator_subtypes import IndicatorSubtypesTable
from tables.indicator_values import IndicatorValuesTable
from tables.population_age_sex import PopulationAgeSexTable

MIN_CHART_YEAR = 2020
MAX_CHART_YEAR = 2025


class AnalyticsRepo:
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
    
    def get_indicators_by_names(
        self,
        session: Session,
        names: list[str],
    ) -> list[IndicatorsTable]:
        if not names:
            return []

        normalized_names = [name.strip().lower() for name in names if name.strip()]
        if not normalized_names:
            return []

        return (
            session.query(IndicatorsTable)
            .outerjoin(IndicatorSubtypesTable, IndicatorsTable.subtype_id == IndicatorSubtypesTable.id)
            .filter(
                (
                    func.lower(IndicatorsTable.name).in_(normalized_names)
                    | func.lower(IndicatorSubtypesTable.name).in_(normalized_names)
                ),
                IndicatorsTable.is_deleted == False,
            )
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
                IndicatorValuesTable.year >= MIN_CHART_YEAR,
                IndicatorValuesTable.year <= MAX_CHART_YEAR,
            )
            .order_by(IndicatorValuesTable.year.asc())
            .all()
        )

    def get_population_rows(
        self,
        session: Session,
        region_id: int,
    ) -> list[PopulationAgeSexTable]:
        return (
            session.query(PopulationAgeSexTable)
            .filter(
                PopulationAgeSexTable.region_id == region_id,
                PopulationAgeSexTable.is_deleted == False,
                PopulationAgeSexTable.year >= MIN_CHART_YEAR,
                PopulationAgeSexTable.year <= MAX_CHART_YEAR,
            )
            .order_by(PopulationAgeSexTable.year.asc(), PopulationAgeSexTable.age_code.asc())
            .all()
        )
