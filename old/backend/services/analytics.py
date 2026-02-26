from collections import defaultdict

from sqlalchemy.orm import Session

from models import (
    ChartDataResponseModel,
    ChartPointModel,
    ChartSeriesModel,
    PopulationPyramidPointModel,
    PopulationPyramidResponseModel,
)
from repo.analytics import AnalyticsRepo


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepo | None = None):
        self.repo = repo or AnalyticsRepo()

    def get_chart_data(
        self,
        session: Session,
        region_id: int,
        indicator_ids: list[int],
    ) -> ChartDataResponseModel:
        region = self.repo.get_region(session=session, region_id=region_id)
        if region is None:
            return ChartDataResponseModel(
                region_id=region_id,
                region_name="Неизвестный регион",
                series=[],
            )

        if not indicator_ids:
            return ChartDataResponseModel(
                region_id=region.id,
                region_name=region.name,
                series=[],
            )

        indicators = self.repo.get_indicators(
            session=session,
            indicator_ids=indicator_ids,
        )
        indicator_values = self.repo.get_indicator_values(
            session=session,
            region_id=region_id,
            indicator_ids=indicator_ids,
        )

        points_by_indicator: dict[int, list[ChartPointModel]] = {
            indicator_id: [] for indicator_id in indicator_ids
        }
        for value in indicator_values:
            points_by_indicator.setdefault(value.indicator_id, []).append(
                ChartPointModel(year=value.year, value=value.value)
            )

        indicators_by_id = {indicator.id: indicator for indicator in indicators}
        ordered_series: list[ChartSeriesModel] = []
        for indicator_id in indicator_ids:
            indicator = indicators_by_id.get(indicator_id)
            if indicator is None:
                continue

            ordered_series.append(
                ChartSeriesModel(
                    indicator_id=indicator.id,
                    indicator_name=indicator.name,
                    points=points_by_indicator.get(indicator.id, []),
                )
            )

        return ChartDataResponseModel(
            region_id=region.id,
            region_name=region.name,
            series=ordered_series,
        )

    def get_population_pyramid(
        self,
        session: Session,
        region_id: int,
        year: int | None,
    ) -> PopulationPyramidResponseModel:
        region = self.repo.get_region(session=session, region_id=region_id)
        if region is None:
            return PopulationPyramidResponseModel(
                region_id=region_id,
                region_name="Неизвестный регион",
                year=year or 0,
                points=[],
            )

        target_year = year
        if target_year is None:
            years = self.repo.get_population_years(session=session, region_id=region_id)
            if not years:
                return PopulationPyramidResponseModel(
                    region_id=region.id,
                    region_name=region.name,
                    year=0,
                    points=[],
                )
            target_year = years[0]

        rows = self.repo.get_population_rows(
            session=session,
            region_id=region_id,
            year=target_year,
        )
        points_map: dict[str, dict[str, float]] = defaultdict(lambda: {"M": 0.0, "F": 0.0, "T": 0.0})

        for row in rows:
            points_map[row.age_code][row.sex_code] = row.value

        points: list[PopulationPyramidPointModel] = []
        for age_code in sorted(points_map.keys()):
            bucket = points_map[age_code]
            total = bucket["T"] if bucket["T"] else bucket["M"] + bucket["F"]
            points.append(
                PopulationPyramidPointModel(
                    age_code=age_code,
                    male=bucket["M"],
                    female=bucket["F"],
                    total=total,
                )
            )

        return PopulationPyramidResponseModel(
            region_id=region.id,
            region_name=region.name,
            year=target_year,
            points=points,
        )
