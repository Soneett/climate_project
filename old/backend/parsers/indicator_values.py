from __future__ import annotations

from pathlib import Path

from sqlalchemy.orm import Session

from tables.data_sources import DataSourcesTable
from tables.indicator_subtypes import IndicatorSubtypesTable
from tables.indicator_values import IndicatorValuesTable
from tables.indicators import IndicatorsTable
from tables.regions import RegionsTable
from tables.units import UnitsTable


INDICATOR_KEY_MAP: dict[str, dict[str, str | None]] = {
    "births_abs": {"name": "Рождаемость", "type": "демография", "theme": "рождаемость, смертность, естественный прирост"},
    "deaths_abs": {"name": "Смертность", "type": "демография", "theme": "рождаемость, смертность, естественный прирост"},
    "infant_deaths_abs": {"name": "Смертность — до 1 года", "type": "демография", "theme": "рождаемость, смертность, естественный прирост"},
    "natural_abs": {"name": "Естественный прирост", "type": "демография", "theme": "рождаемость, смертность, естественный прирост"},
    "death_rate_all_causes": {"name": "Смертность — все причины", "type": "демография", "theme": "причины смерти"},
    "death_rate_circulatory_diseases": {"name": "Смертность — болезни системы кровообращения", "type": "демография", "theme": "причины смерти"},
    "death_rate_neoplasms": {"name": "Смертность — новообразования", "type": "демография", "theme": "причины смерти"},
    "death_rate_external_causes": {"name": "Смертность — внешние причины", "type": "демография", "theme": "причины смерти"},
    "death_rate_transport_injuries_all": {"name": "Смертность — транспортные травмы", "type": "демография", "theme": "причины смерти"},
    "death_rate_road_accidents": {"name": "Смертность — ДТП", "type": "демография", "theme": "причины смерти"},
    "death_rate_alcohol_poisoning": {"name": "Смертность — отравления алкоголем", "type": "демография", "theme": "причины смерти"},
    "death_rate_suicides": {"name": "Смертность — самоубийства", "type": "демография", "theme": "причины смерти"},
    "death_rate_homicides": {"name": "Смертность — убийства", "type": "демография", "theme": "причины смерти"},
    "death_rate_respiratory_diseases": {"name": "Смертность — болезни органов дыхания", "type": "демография", "theme": "причины смерти"},
    "death_rate_digestive_diseases": {"name": "Смертность — болезни органов пищеварения", "type": "демография", "theme": "причины смерти"},
    "death_rate_infectious_parasitic": {"name": "Смертность — инфекционные и паразитарные болезни", "type": "демография", "theme": "причины смерти"},
    "death_rate_tuberculosis": {"name": "Смертность — туберкулез", "type": "демография", "theme": "причины смерти"},
}


FILE_SOURCE_MAP = {
    "morbidity": "Заболеваемость по основным классам болезней",
    "road_press_release": "Автомобильные дороги и транспортная инфраструктура",
    "structure_of_income": "Состав и структура денежных доходов и расходов населения",
    "kmn_population": "Оценка численности коренных малочисленных народов",
    "migration": "Общие итоги миграции населения",
    "IVBO": "Индекс выпуска товаров и услуг по базовым видам экономической деятельности",
    "poverty_level": "Население с денежными доходами ниже границы бедности",
    "vrp": "Валовой региональный продукт",
    "healthcare_indicators": "Основные показатели здравоохранения",
}

FILE_TYPE_THEME_MAP = {
    "morbidity": ("здравоохранение", "заболеваемость"),
    "road_press_release": ("инфраструктура", "автомобильные дороги"),
    "structure_of_income": ("уровень жизни", "доходы и расходы"),
    "consumption_expenses": ("уровень жизни", "доходы и расходы"),
    "kmn_population": ("демография", "численность населения"),
    "migration": ("демография", "миграция"),
    "IVBO": ("экономика", "деловая активность"),
    "poverty_level": ("уровень жизни", "бедность"),
    "vrp": ("экономика", "валовой региональный продукт"),
    "healthcare_indicators": ("здравоохранение", "кадровые и инфраструктурные показатели"),
    "death_causes": ("демография", "причины смерти"),
    "birth_abs": ("демография", "рождаемость, смертность, естественный прирост"),
    "deaths": ("демография", "рождаемость, смертность, естественный прирост"),
    "natural_abs": ("демография", "рождаемость, смертность, естественный прирост"),
}


def _normalize_name(value: str | None) -> str:
    return (value or "").replace("-всего", "").strip()


def _normalize_indicator_name(raw_name: str) -> tuple[str, str | None]:
    clean_name = raw_name.strip()
    if "—" not in clean_name:
        return clean_name, None

    base_name, subtype_part = clean_name.split("—", 1)
    subtype = subtype_part.split(",", 1)[0].strip()
    return base_name.strip(), subtype or None


def _resolve_indicator_payload(row: dict, file_stem: str) -> tuple[str, str | None, str | None, str | None] | None:
    indicator_name = row.get("indicator_name")
    if indicator_name:
        name, subtype_name = _normalize_indicator_name(str(indicator_name))
        indicator_type, indicator_theme = FILE_TYPE_THEME_MAP.get(file_stem, ("авто-добавленный", "импорт indicator_values"))
        return name, subtype_name, indicator_type, indicator_theme

    indicator_key = row.get("indicator_key")
    if not indicator_key:
        return None

    mapped = INDICATOR_KEY_MAP.get(str(indicator_key))
    if mapped is None:
        return None

    name, subtype_name = _normalize_indicator_name(str(mapped["name"]))
    return name, subtype_name, mapped.get("type"), mapped.get("theme")


def parse_indicator_values(data: dict, session: Session, source_file: str | None = None):
    metadata = data.get("metadata", {}) or {}
    file_stem = Path(source_file).stem if source_file else ""

    region_name = _normalize_name(metadata.get("region_name"))
    source_name = _normalize_name(metadata.get("source_name")) or _normalize_name(FILE_SOURCE_MAP.get(file_stem))

    rows = data.get("indicator_values", {}).get("rows", [])
    if not rows:
        return

    regions_map = {_normalize_name(r.name): r.id for r in session.query(RegionsTable).all()}
    sources_map = {_normalize_name(s.name): s.id for s in session.query(DataSourcesTable).all()}
    units_map = {_normalize_name(u.code): u.id for u in session.query(UnitsTable).all()}
    indicators_map = {_normalize_name(i.name): i for i in session.query(IndicatorsTable).all()}
    subtypes_map = {_normalize_name(s.name): s.id for s in session.query(IndicatorSubtypesTable).all()}

    if source_name and source_name not in sources_map:
        source = DataSourcesTable(name=source_name, organization="Не указан")
        session.add(source)
        session.flush()
        sources_map[source_name] = source.id

    for row in rows:
        row_region = _normalize_name(row.get("region_name")) or region_name
        row_source = _normalize_name(row.get("source_name")) or source_name
        if not row_region or not row_source:
            continue

        region_id = regions_map.get(row_region)
        if not region_id:
            continue

        source_id = sources_map.get(row_source)
        if source_id is None:
            source = DataSourcesTable(name=row_source, organization="Не указан")
            session.add(source)
            session.flush()
            source_id = source.id
            sources_map[row_source] = source_id

        resolved = _resolve_indicator_payload(row=row, file_stem=file_stem)
        if not resolved:
            continue

        indicator_name, subtype_name, indicator_type, indicator_theme = resolved

        unit_code = _normalize_name(row.get("unit_code"))
        unit_id = None
        if unit_code:
            unit_id = units_map.get(unit_code)
            if unit_id is None:
                unit = UnitsTable(code=unit_code, name=unit_code)
                session.add(unit)
                session.flush()
                unit_id = unit.id
                units_map[unit_code] = unit_id

        indicator = indicators_map.get(indicator_name)
        if indicator is None:
            indicator = IndicatorsTable(
                name=indicator_name,
                type=indicator_type or "авто-добавленный",
                theme=indicator_theme or "импорт indicator_values",
                unit_id=unit_id,
                subtype_id=None,
            )
            session.add(indicator)
            session.flush()
            indicators_map[indicator_name] = indicator
        else:
            if indicator.unit_id is None and unit_id is not None:
                indicator.unit_id = unit_id
            if not indicator.type and indicator_type:
                indicator.type = indicator_type
            if not indicator.theme and indicator_theme:
                indicator.theme = indicator_theme

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

        year = row.get("year")
        value = row.get("value")
        if year is None or value is None:
            continue

        session.add(
            IndicatorValuesTable(
                region_id=region_id,
                indicator_id=indicator.id,
                year=int(year),
                value=float(value),
                source_id=source_id,
            )
        )
