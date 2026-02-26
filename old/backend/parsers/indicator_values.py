from __future__ import annotations

from sqlalchemy.orm import Session

from tables.indicator_values import IndicatorValuesTable
from tables.indicator_subtypes import IndicatorSubtypesTable
from tables.indicators import IndicatorsTable
from tables.regions import RegionsTable
from tables.data_sources import DataSourcesTable
from tables.units import UnitsTable


INDICATOR_KEY_MAP = {
    "births_abs": "Рождаемость",
    "deaths_abs": "Смертность",
    "infant_deaths_abs": "Смертность — до 1 года",
    "natural_abs": "Естественный прирост",
    "death_rate_all_causes": "Смертность — все причины",
    "death_rate_circulatory_diseases": "Смертность — болезни системы кровообращения",
    "death_rate_neoplasms": "Смертность — новообразования",
    "death_rate_external_causes": "Смертность — внешние причины",
    "death_rate_transport_injuries_all": "Смертность — транспортные травмы",
    "death_rate_road_accidents": "Смертность — ДТП",
    "death_rate_alcohol_poisoning": "Смертность — отравления алкоголем",
    "death_rate_suicides": "Смертность — самоубийства",
    "death_rate_homicides": "Смертность — убийства",
    "death_rate_respiratory_diseases": "Смертность — болезни органов дыхания",
    "death_rate_digestive_diseases": "Смертность — болезни органов пищеварения",
    "death_rate_infectious_parasitic": "Смертность — инфекционные и паразитарные болезни",
    "death_rate_tuberculosis": "Смертность — туберкулез",
}


def _normalize_indicator_name(raw_name: str) -> tuple[str, str | None]:
    clean_name = raw_name.strip()
    if "—" not in clean_name:
        return clean_name, None

    base_name, subtype_part = clean_name.split("—", 1)
    subtype = subtype_part.split(",", 1)[0].strip()
    return base_name.strip(), subtype or None


def _resolve_indicator_name(row: dict) -> tuple[str, str | None] | None:
    if "indicator_name" in row and row["indicator_name"]:
        return _normalize_indicator_name(str(row["indicator_name"]))

    key = row.get("indicator_key")
    if not key:
        return None

    mapped = INDICATOR_KEY_MAP.get(key)
    if not mapped:
        return None

    return _normalize_indicator_name(mapped)


def parse_indicator_values(data: dict, session: Session):
    metadata = data.get("metadata", {})
    region_name = metadata.get("region_name")
    source_name = metadata.get("source_name")

    rows = data.get("indicator_values", {}).get("rows", [])
    if not rows:
        return

    regions_map = {r.name.strip(): r.id for r in session.query(RegionsTable).all()}
    sources_map = {s.name.strip(): s.id for s in session.query(DataSourcesTable).all()}
    units_map = {u.code.strip(): u.id for u in session.query(UnitsTable).all()}

    indicators_map = {i.name.strip(): i for i in session.query(IndicatorsTable).all()}
    subtypes_map = {s.name.strip(): s.id for s in session.query(IndicatorSubtypesTable).all()}

    for row in rows:
        row_region = (row.get("region_name") or region_name or "").replace("-всего", "").strip()
        row_source = (row.get("source_name") or source_name or "").strip()
        if not row_region or not row_source:
            continue

        region_id = regions_map.get(row_region)
        source_id = sources_map.get(row_source)
        if not region_id or not source_id:
            continue

        resolved = _resolve_indicator_name(row)
        if not resolved:
            continue

        indicator_name, subtype_name = resolved

        indicator = indicators_map.get(indicator_name)
        if indicator is None:
            indicator = IndicatorsTable(
                name=indicator_name,
                type="авто-добавленный",
                theme="импорт indicator_values",
                unit_id=units_map.get(row.get("unit_code", "").strip()) if row.get("unit_code") else None,
                subtype_id=None,
            )
            session.add(indicator)
            session.flush()
            indicators_map[indicator_name] = indicator

        subtype_id = None
        if subtype_name:
            subtype_id = subtypes_map.get(subtype_name)
            if subtype_id is None:
                subtype = IndicatorSubtypesTable(name=subtype_name)
                session.add(subtype)
                session.flush()
                subtype_id = subtype.id
                subtypes_map[subtype_name] = subtype_id

            if indicator.subtype_id is None:
                indicator.subtype_id = subtype_id

        session.add(
            IndicatorValuesTable(
                region_id=region_id,
                indicator_id=indicator.id,
                year=row["year"],
                value=row["value"],
                source_id=source_id,
            )
        )
