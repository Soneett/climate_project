from collections import defaultdict
from dataclasses import dataclass
import re

from sqlalchemy.orm import Session

from models import (
    LineChartDatasetModel,
    LineChartResponseModel,
    PieChartResponseModel,
    PieTimelinePointModel,
    PieTimelineSeriesItemModel,
    WaffleChartResponseModel,
    WaffleChartTimelinePointModel,
    WaffleChartTimelineSeriesItemModel,
    PopulationPyramidResponseModel,
    PopulationPyramidTimelinePointModel,
    StackPlotResponseModel,
    StackPlotSeriesItemModel,
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


@dataclass
class IndicatorSelection:
    indicator_term: str
    subtype_patterns: list[str]


class AnalyticsService:
    def __init__(self, repo: AnalyticsRepo | None = None):
        self.repo = repo or AnalyticsRepo()

    @staticmethod
    def _parse_indicators(indicators: str | list[str]) -> list[str]:
        if isinstance(indicators, list):
            return [str(part).strip() for part in indicators if str(part).strip()]
        return [part.strip() for part in str(indicators).split(",") if part.strip()]

    @staticmethod
    def _parse_indicator_selections(indicators: str | list[str]) -> list[IndicatorSelection]:
        selections: list[IndicatorSelection] = []
        for raw_value in AnalyticsService._parse_indicators(indicators):
            if ":" not in raw_value:
                selections.append(IndicatorSelection(indicator_term=raw_value, subtype_patterns=[]))
                continue

            indicator_term, patterns_csv = raw_value.split(":", 1)
            patterns = [pattern.strip() for pattern in patterns_csv.split("|") if pattern.strip()]
            selections.append(
                IndicatorSelection(
                    indicator_term=indicator_term.strip(),
                    subtype_patterns=patterns,
                )
            )
        return selections

    @staticmethod
    def _build_regex(pattern: str) -> re.Pattern[str] | None:
        if pattern == "*":
            return re.compile(".*", re.IGNORECASE)

        prepared = pattern.strip()
        if not prepared:
            return None

        if "*" in prepared and ".*" not in prepared:
            prepared = prepared.replace("*", ".*")

        try:
            return re.compile(prepared, re.IGNORECASE)
        except re.error:
            return None

    def _resolve_indicator_ids(
        self,
        session: Session,
        indicators: str | list[str],
    ) -> list[int]:
        selections = self._parse_indicator_selections(indicators)
        names = [selection.indicator_term for selection in selections]
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
        normalized_patterns_by_name: dict[str, list[str]] = {
            _normalize_indicator_term(selection.indicator_term): selection.subtype_patterns
            for selection in selections
        }
        subtype_ids = [indicator.subtype_id for indicator in resolved if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: _normalize_indicator_term(subtype.name)
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}

        for name in normalized_names:
            exact_name_matches = []
            exact_subtype_matches = []
            fuzzy_matches = []
            for indicator in resolved:
                indicator_name = _normalize_indicator_term(indicator.name)
                subtype_name = subtype_map.get(indicator.subtype_id) if indicator.subtype_id is not None else ""

                if indicator_name == name:
                    exact_name_matches.append(indicator)
                    continue

                if subtype_name and subtype_name == name:
                    exact_subtype_matches.append(indicator)
                    continue

                if name in indicator_name or (subtype_name and name in subtype_name):
                    fuzzy_matches.append(indicator)

            same_name = exact_name_matches or exact_subtype_matches or fuzzy_matches

            if same_name:
                selected_patterns = normalized_patterns_by_name.get(name, [])

                if selected_patterns:
                    regex_patterns = [
                        compiled
                        for compiled in (self._build_regex(pattern) for pattern in selected_patterns)
                        if compiled is not None
                    ]
                    filtered = []
                    for indicator in same_name:
                        subtype_name = subtype_map.get(indicator.subtype_id, "")
                        indicator_name = _normalize_indicator_term(indicator.name)

                        if regex_patterns and any(
                            pattern.fullmatch(subtype_name)
                            or pattern.search(subtype_name)
                            or pattern.fullmatch(indicator_name)
                            or pattern.search(indicator_name)
                            for pattern in regex_patterns
                        ):
                            filtered.append(indicator.id)
                    candidate_ids = filtered
                elif exact_name_matches:
                    base_indicators = [indicator.id for indicator in exact_name_matches if indicator.subtype_id is None]
                    candidate_ids = base_indicators or [indicator.id for indicator in exact_name_matches]
                elif exact_subtype_matches:
                    candidate_ids = [indicator.id for indicator in exact_subtype_matches]
                else:
                    base_indicators = [indicator.id for indicator in fuzzy_matches if indicator.subtype_id is None]
                    candidate_ids = base_indicators or [indicator.id for indicator in fuzzy_matches]
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
        indicators: str | list[str],
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
        indicators: str | list[str],
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

        indicator_names = self._build_unique_indicator_labels(indicators, subtype_map)

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

        midpoint = (len(indicator_ids) + 1) // 2
        legend_items = [indicator_names[indicator_id] for indicator_id in indicator_ids if indicator_id in indicator_names]
        return PieChartResponseModel(
            timelineLabels=timeline_labels,
            legendLeftItems=legend_items[:midpoint],
            legendRightItems=legend_items[midpoint:],
            timelineData=timeline_data,
        )

    def get_waffle_chart_data(
        self,
        session: Session,
        region_id: int,
        indicators: str | list[str],
    ) -> WaffleChartResponseModel:
        indicator_ids = self._resolve_indicator_ids(session=session, indicators=indicators)
        if not indicator_ids:
            return WaffleChartResponseModel(timelineLabels=[], timelineData=[])

        values = self.repo.get_indicator_values(session=session, region_id=region_id, indicator_ids=indicator_ids)
        if not values:
            return WaffleChartResponseModel(timelineLabels=[], timelineData=[])

        indicators_rows = self.repo.get_indicators(session=session, indicator_ids=indicator_ids)
        subtype_ids = [indicator.subtype_id for indicator in indicators_rows if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: subtype.name
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}

        indicator_names = self._build_unique_indicator_labels(indicators_rows, subtype_map)

        grouped_by_year: dict[int, dict[int, float]] = defaultdict(dict)
        for row in values:
            grouped_by_year[row.year][row.indicator_id] = float(row.value)

        timeline_labels = [str(year) for year in sorted(grouped_by_year.keys())]
        timeline_data: list[WaffleChartTimelinePointModel] = []

        for year in sorted(grouped_by_year.keys()):
            year_total = sum(grouped_by_year[year].get(indicator_id, 0.0) for indicator_id in indicator_ids)
            points: list[WaffleChartTimelineSeriesItemModel] = []
            for indicator_id in indicator_ids:
                if indicator_id not in indicator_names:
                    continue
                absolute_value = grouped_by_year[year].get(indicator_id, 0.0)
                percentage_value = (absolute_value / year_total * 100.0) if year_total else 0.0
                points.append(
                    WaffleChartTimelineSeriesItemModel(
                        name=indicator_names[indicator_id],
                        value=percentage_value,
                        absoluteValue=absolute_value,
                    )
                )

            timeline_data.append(WaffleChartTimelinePointModel(data=points))

        return WaffleChartResponseModel(
            timelineLabels=timeline_labels,
            timelineData=timeline_data,
        )

    @staticmethod
    def _build_unique_indicator_labels(indicators, subtype_map: dict[int, str]) -> dict[int, str]:
        labels: dict[int, str] = {}
        raw_labels: dict[int, str] = {}
        for indicator in indicators:
            subtype_name = subtype_map.get(indicator.subtype_id) if indicator.subtype_id is not None else None
            raw_labels[indicator.id] = f"{indicator.name} — {subtype_name}" if subtype_name else indicator.name

        label_counts: dict[str, int] = defaultdict(int)
        for label in raw_labels.values():
            label_counts[label] += 1

        for indicator in indicators:
            label = raw_labels[indicator.id]
            if label_counts[label] > 1:
                label = f"{label} (#{indicator.id})"
            labels[indicator.id] = label
        return labels

    def get_stack_plot_data(
        self,
        session: Session,
        region_id: int,
        indicators: str | list[str],
    ) -> StackPlotResponseModel:
        indicator_ids = self._resolve_indicator_ids(session=session, indicators=indicators)
        if not indicator_ids:
            return StackPlotResponseModel(timelineLabels=[], legendItems=[], seriesData=[])

        values = self.repo.get_indicator_values(session=session, region_id=region_id, indicator_ids=indicator_ids)
        if not values:
            values = self.repo.get_indicator_values_without_year_bounds(
                session=session,
                region_id=region_id,
                indicator_ids=indicator_ids,
            )
        if not values:
            return StackPlotResponseModel(timelineLabels=[], legendItems=[], seriesData=[])

        indicators_rows = self.repo.get_indicators(session=session, indicator_ids=indicator_ids)
        subtype_ids = [indicator.subtype_id for indicator in indicators_rows if indicator.subtype_id is not None]
        subtype_map = {
            subtype.id: subtype.name
            for subtype in session.query(IndicatorSubtypesTable)
            .filter(IndicatorSubtypesTable.id.in_(subtype_ids), IndicatorSubtypesTable.is_deleted == False)
            .all()
        } if subtype_ids else {}
        indicator_names = self._build_unique_indicator_labels(indicators_rows, subtype_map)

        grouped: dict[int, dict[int, float]] = defaultdict(dict)
        for row in values:
            grouped[row.indicator_id][row.year] = float(row.value)
        years = sorted({row.year for row in values})

        series = [
            StackPlotSeriesItemModel(
                name=indicator_names[indicator_id],
                data=[grouped[indicator_id].get(year, 0.0) for year in years],
            )
            for indicator_id in indicator_ids
            if indicator_id in indicator_names
        ]

        legend_items = [item.name for item in series]
        timeline_labels = [str(year) for year in years]
        return StackPlotResponseModel(timelineLabels=timeline_labels, legendItems=legend_items, seriesData=series)

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
