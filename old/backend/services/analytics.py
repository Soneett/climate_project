from collections import defaultdict
import re

from sqlalchemy.orm import Session

from models import (
    LineChartDatasetModel,
    LineChartResponseModel,
    PieChartResponseModel,
    PieTimelinePointModel,
    PieTimelineSeriesItemModel,
    PopulationPyramidResponseModel,
    PopulationPyramidTimelinePointModel,
)
from repo.analytics import AnalyticsRepo
from tables.indicator_subtypes import IndicatorSubtypesTable

_INDICATOR_ALIASES: dict[str, list[str]] = {
    "сердечно-сосудистые": ["болезни системы кровообращения"],
    "онкологические": ["новообразования"],
    "несчастные случаи": ["внешние причины"],
    "города": ["городское население", "город"],
    "районы": ["район"],
    "сельские поселения": ["сельское население", "село"],
}


def _normalize_indicator_term(value: str) -> str:
    normalized = value.strip().lower().replace("ё", "е")
    normalized = normalized.replace("–", "-").replace("—", "-")
    normalized = re.sub(r"[^\w\s\-]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _is_age_interval(age_code: str) -> bool:
    normalized = age_code.strip().replace('–', '-').replace('—', '-')
    return bool(re.fullmatch(r"(\d+)\s*-\s*(\d+)", normalized) or re.fullmatch(r"(\d+)\s*\+", normalized))


def _age_sort_key(age_code: str) -> tuple[int, int, str]:
    normalized = age_code.strip().replace('–', '-').replace('—', '-')
    range_match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", normalized)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        return (0, start * 1000 + end, normalized)

    plus_match = re.fullmatch(r"(\d+)\s*\+", normalized)
    if plus_match:
        start = int(plus_match.group(1))
        return (1, start, normalized)

    return (2, 10**9, normalized)


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepo | None = None):
        self.repo = repo or AnalyticsRepo()

    @staticmethod
    def _parse_indicators(indicators: str) -> list[str]:
        return [part.strip() for part in indicators.split(",") if part.strip()]

    def _resolve_indicator_ids(
        self,
        session: Session,
        indicators: str,
    ) -> list[int]:
        names = self._parse_indicators(indicators)
        if not names:
            return []

        expanded_names: list[str] = []
        for name in names:
            expanded_names.append(name)
            alias_candidates = _INDICATOR_ALIASES.get(_normalize_indicator_term(name), [])
            expanded_names.extend(alias_candidates)

        deduplicated_names = list(dict.fromkeys(expanded_names))
        resolved = self.repo.get_indicators_by_names(session=session, names=deduplicated_names)
        ordered_ids: list[int] = []
        normalized_names = [_normalize_indicator_term(name) for name in names]
        subtype_ids = [indicator.subtype_id for indicator in resolved if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: _normalize_indicator_term(subtype.name)
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}

        for name in normalized_names:
            same_name = []
            for indicator in resolved:
                indicator_name = _normalize_indicator_term(indicator.name)
                subtype_name = subtype_map.get(indicator.subtype_id) if indicator.subtype_id is not None else ""
                if (
                    indicator_name == name
                    or (subtype_name and subtype_name == name)
                    or name in indicator_name
                    or (subtype_name and name in subtype_name)
                ):
                    same_name.append(indicator)

            if same_name:
                subindicators = [indicator.id for indicator in same_name if indicator.subtype_id is not None]
                candidate_ids = subindicators or [indicator.id for indicator in same_name]
            else:
                candidate_ids = []

            for candidate_id in candidate_ids:
                if candidate_id not in ordered_ids:
                    ordered_ids.append(candidate_id)

        if ordered_ids:
            return ordered_ids

        return [indicator.id for indicator in resolved]

    def get_line_chart_data(
        self,
        session: Session,
        region_id: int,
        indicators: str,
    ) -> LineChartResponseModel:
        indicator_ids = self._resolve_indicator_ids(session=session, indicators=indicators)
        if not indicator_ids:
            return LineChartResponseModel(labels=[], datasets=[])

        values = self.repo.get_indicator_values(session=session, region_id=region_id, indicator_ids=indicator_ids)
        if not values:
            return LineChartResponseModel(labels=[], datasets=[])

        indicators = self.repo.get_indicators(session=session, indicator_ids=indicator_ids)

        labels = sorted({str(value.year) for value in values})
        indicator_names = {indicator.id: indicator.name for indicator in indicators}

        subtype_ids = [indicator.subtype_id for indicator in indicators if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: subtype.name
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}

        grouped: dict[int, dict[int, float]] = defaultdict(dict)
        for value in values:
            grouped[value.indicator_id][value.year] = value.value

        datasets: list[LineChartDatasetModel] = []
        years_int = [int(label) for label in labels]
        for indicator_id in indicator_ids:
            name = indicator_names.get(indicator_id)
            if not name:
                continue

            subtype_name = subtype_map.get(next((i.subtype_id for i in indicators if i.id == indicator_id), None))
            dataset_name = f"{name} — {subtype_name}" if subtype_name else name

            data = [float(grouped[indicator_id].get(year, 0.0)) for year in years_int]
            datasets.append(LineChartDatasetModel(name=dataset_name, data=data))

        return LineChartResponseModel(labels=labels, datasets=datasets)

    def get_pie_chart_data(
        self,
        session: Session,
        region_id: int,
        indicators: str,
    ) -> PieChartResponseModel:
        indicator_ids = self._resolve_indicator_ids(session=session, indicators=indicators)
        if not indicator_ids:
            return PieChartResponseModel(timelineLabels=[], timelineData=[])

        values = self.repo.get_indicator_values(session=session, region_id=region_id, indicator_ids=indicator_ids)
        if not values:
            return PieChartResponseModel(timelineLabels=[], timelineData=[])

        indicators = self.repo.get_indicators(session=session, indicator_ids=indicator_ids)

        subtype_ids = [indicator.subtype_id for indicator in indicators if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: subtype.name
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}

        indicator_names = {
            indicator.id: (subtype_map.get(indicator.subtype_id) or indicator.name)
            for indicator in indicators
        }

        grouped_by_year: dict[int, dict[int, float]] = defaultdict(dict)
        for row in values:
            grouped_by_year[row.year][row.indicator_id] = float(row.value)

        timeline_labels = [str(year) for year in sorted(grouped_by_year.keys())]
        timeline_data: list[PieTimelinePointModel] = []

        for year in sorted(grouped_by_year.keys()):
            points = [
                PieTimelineSeriesItemModel(
                    name=indicator_names[indicator_id],
                    value=grouped_by_year[year].get(indicator_id, 0.0),
                )
                for indicator_id in indicator_ids
                if indicator_id in indicator_names
            ]
            timeline_data.append(
                PieTimelinePointModel(
                    title={"text": f"Распределение — {year}"},
                    series=[{"data": points}],
                )
            )

        return PieChartResponseModel(timelineLabels=timeline_labels, timelineData=timeline_data)

    def get_population_pyramid(
        self,
        session: Session,
        region_id: int,
    ) -> PopulationPyramidResponseModel:
        rows = self.repo.get_population_rows(session=session, region_id=region_id)

        grouped: dict[int, dict[str, dict[str, float]]] = defaultdict(lambda: defaultdict(lambda: {"M": 0.0, "F": 0.0}))
        for row in rows:
            if not _is_age_interval(row.age_code):
                continue
            grouped[row.year][row.age_code][row.sex_code] = float(row.value)

        timeline_labels = [str(year) for year in sorted(grouped.keys())]
        categories = sorted(
            {age_code for yearly in grouped.values() for age_code in yearly.keys()},
            key=_age_sort_key,
        )

        timeline_data: list[PopulationPyramidTimelinePointModel] = []
        for year in sorted(grouped.keys()):
            male = []
            female = []
            for age_code in categories:
                male.append(-abs(grouped[year][age_code].get("M", 0.0)))
                female.append(abs(grouped[year][age_code].get("F", 0.0)))

            timeline_data.append(
                PopulationPyramidTimelinePointModel(
                    title={"text": f"Половозрастная структура — {year}"},
                    series=[{"data": male}, {"data": female}],
                )
            )

        return PopulationPyramidResponseModel(
            categories=categories,
            legendItems=["Мужчины", "Женщины"],
            timelineLabels=timeline_labels,
            timelineData=timeline_data,
        )
