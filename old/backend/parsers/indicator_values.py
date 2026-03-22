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
    "death_rate_all_causes": {"name": "Причины смертности — все причины", "type": "демография", "theme": "причины смерти"},
    "death_rate_circulatory_diseases": {"name": "Причины смертности — болезни системы кровообращения", "type": "демография", "theme": "причины смерти"},
    "death_rate_neoplasms": {"name": "Причины смертности — новообразования", "type": "демография", "theme": "причины смерти"},
    "death_rate_external_causes": {"name": "Причины смертности — внешние причины", "type": "демография", "theme": "причины смерти"},
    "death_rate_transport_injuries_all": {"name": "Причины смертности — транспортные травмы", "type": "демография", "theme": "причины смерти"},
    "death_rate_road_accidents": {"name": "Причины смертности — ДТП", "type": "демография", "theme": "причины смерти"},
    "death_rate_alcohol_poisoning": {"name": "Причины смертности — отравления алкоголем", "type": "демография", "theme": "причины смерти"},
    "death_rate_suicides": {"name": "Причины смертности — самоубийства", "type": "демография", "theme": "причины смерти"},
    "death_rate_homicides": {"name": "Причины смертности — убийства", "type": "демография", "theme": "причины смерти"},
    "death_rate_respiratory_diseases": {"name": "Причины смертности — болезни органов дыхания", "type": "демография", "theme": "причины смерти"},
    "death_rate_digestive_diseases": {"name": "Причины смертности — болезни органов пищеварения", "type": "демография", "theme": "причины смерти"},
    "death_rate_infectious_parasitic": {"name": "Причины смертности — инфекционные и паразитарные болезни", "type": "демография", "theme": "причины смерти"},
    "death_rate_tuberculosis": {"name": "Причины смертности — туберкулез", "type": "демография", "theme": "причины смерти"},
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
    "agri_price_indices": "Индексы цен производителей сельскохозяйственной продукции",
    "birth_abs": "Демографические показатели: рождаемость, смертность, естественный прирост",
    "cpi": "Индексы потребительских цен",
    "credit_debit_structure": "Кредитно-дебетная структура денежных доходов и расходов населения",
    "death_causes": "Причины смертности населения",
    "deaths": "Демографические показатели: рождаемость, смертность, естественный прирост",
    "demo_org": "Демография организаций",
    "employment_education": "Занятость населения по уровню образования",
    "hightech_share_vrp": "Доля высокотехнологичных и наукоемких отраслей в ВРП",
    "housing_fund_movement": "Движение жилищного фонда",
    "natural_abs": "Демографические показатели: рождаемость, смертность, естественный прирост",
    "org_liquidation": "Ликвидация организаций",
    "org_ownership": "Структура организаций по формам собственности",
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


def _normalize_text(value: str | None) -> str:
    return (value or "").strip()


def _normalize_region_name(value: str | None) -> str:
    return _normalize_text(value).replace("-всего", "")


def _split_indicator(raw_name: str) -> tuple[str, str | None]:
    clean_name = _normalize_text(raw_name)
    if "—" not in clean_name:
        return clean_name, None

    base_name, subtype_part = clean_name.split("—", 1)
    subtype = subtype_part.split(",", 1)[0].strip()
    return base_name.strip(), subtype or None


def _resolve_indicator_payload(
    row: dict,
    file_stem: str,
    default_indicator_type: str | None = None,
    default_indicator_theme: str | None = None,
) -> tuple[str, str | None, str | None, str | None] | None:
    indicator_name = row.get("indicator_name")
    if indicator_name:
        base_name, subtype_name = _split_indicator(str(indicator_name))
        indicator_type, indicator_theme = (
            default_indicator_type,
            default_indicator_theme,
        )
        if not indicator_type or not indicator_theme:
            indicator_type, indicator_theme = FILE_TYPE_THEME_MAP.get(file_stem, ("авто-добавленный", "импорт indicator_values"))
        return base_name, subtype_name, indicator_type, indicator_theme

    indicator_key = row.get("indicator_key")
    if not indicator_key:
        return None

    mapped = INDICATOR_KEY_MAP.get(str(indicator_key))
    if mapped is None:
        return None

    base_name, subtype_name = _split_indicator(str(mapped["name"]))
    return base_name, subtype_name, mapped.get("type"), mapped.get("theme")


def _next_id(session: Session, table) -> int:
    max_id = session.query(table.id).order_by(table.id.desc()).first()
    return (max_id[0] + 1) if max_id else 1


def parse_indicator_values(data: dict, session: Session, source_file: str | None = None):
    metadata = data.get("metadata", {}) or {}
    file_stem = Path(source_file).stem if source_file else ""

    region_name = _normalize_region_name(metadata.get("region_name"))
    source_name = _normalize_text(metadata.get("source_name")) or _normalize_text(FILE_SOURCE_MAP.get(file_stem))
    default_indicator_type = _normalize_text(metadata.get("indicator_type"))
    default_indicator_theme = _normalize_text(metadata.get("indicator_theme"))
    if not default_indicator_type or not default_indicator_theme:
        mapped_type, mapped_theme = FILE_TYPE_THEME_MAP.get(file_stem, ("", ""))
        default_indicator_type = default_indicator_type or mapped_type
        default_indicator_theme = default_indicator_theme or mapped_theme
    if not source_name:
        source_name = f"Источник не указан ({file_stem or 'indicator_values'})"

    rows = data.get("indicator_values", {}).get("rows", [])
    if not rows:
        return

    regions_map = {_normalize_region_name(r.name): r.id for r in session.query(RegionsTable).all()}
    sources_map = {_normalize_text(s.name): s.id for s in session.query(DataSourcesTable).all()}
    units_map = {_normalize_text(u.code): u.id for u in session.query(UnitsTable).all()}
    subtypes_map = {_normalize_text(s.name): s.id for s in session.query(IndicatorSubtypesTable).all()}

    indicators_map: dict[tuple[str, int | None], IndicatorsTable] = {
        (_normalize_text(i.name), i.subtype_id): i
        for i in session.query(IndicatorsTable).all()
    }
    existing_indicator_values = {
        (
            row.region_id,
            row.indicator_id,
            row.year,
            row.source_id,
        ): row
        for row in session.query(IndicatorValuesTable).all()
    }

    if source_name and source_name not in sources_map:
        source = DataSourcesTable(id=_next_id(session, DataSourcesTable), name=source_name, organization="Не указан")
        session.add(source)
        session.flush()
        sources_map[source_name] = source.id

    for row in rows:
        row_region = _normalize_region_name(row.get("region_name")) or region_name
        row_source = _normalize_text(row.get("source_name")) or source_name
        if not row_region:
            continue
        if not row_source:
            row_source = source_name

        region_id = regions_map.get(row_region)
        if not region_id:
            continue

        source_id = sources_map.get(row_source)
        if source_id is None:
            source = DataSourcesTable(id=_next_id(session, DataSourcesTable), name=row_source, organization="Не указан")
            session.add(source)
            session.flush()
            source_id = source.id
            sources_map[row_source] = source_id

        resolved = _resolve_indicator_payload(
            row=row,
            file_stem=file_stem,
            default_indicator_type=default_indicator_type,
            default_indicator_theme=default_indicator_theme,
        )
        if not resolved:
            continue

        indicator_name, subtype_name, indicator_type, indicator_theme = resolved

        unit_code = _normalize_text(row.get("unit_code"))
        unit_id = None
        if unit_code:
            unit_id = units_map.get(unit_code)
            if unit_id is None:
                unit = UnitsTable(id=_next_id(session, UnitsTable), code=unit_code, name=unit_code)
                session.add(unit)
                session.flush()
                unit_id = unit.id
                units_map[unit_code] = unit_id

        subtype_id = None
        if subtype_name:
            subtype_id = subtypes_map.get(subtype_name)
            if subtype_id is None:
                subtype = IndicatorSubtypesTable(id=_next_id(session, IndicatorSubtypesTable), name=subtype_name)
                session.add(subtype)
                session.flush()
                subtype_id = subtype.id
                subtypes_map[subtype_name] = subtype_id

        indicator_key = (indicator_name, subtype_id)
        indicator = indicators_map.get(indicator_key)
        if indicator is None:
            indicator = IndicatorsTable(
                name=indicator_name,
                type=indicator_type,
                theme=indicator_theme,
                unit_id=unit_id,
                subtype_id=subtype_id,
            )
            session.add(indicator)
            session.flush()
            indicators_map[indicator_key] = indicator
        else:
            if indicator.unit_id is None and unit_id is not None:
                indicator.unit_id = unit_id
            if not indicator.type and indicator_type:
                indicator.type = indicator_type
            if not indicator.theme and indicator_theme:
                indicator.theme = indicator_theme

        year = row.get("year")
        value = row.get("value")
        if year is None or value is None:
            continue

        value_key = (
            region_id,
            indicator.id,
            int(year),
            source_id,
        )
        if value_key in existing_indicator_values:
            continue

        indicator_value = IndicatorValuesTable(
            region_id=region_id,
            indicator_id=indicator.id,
            year=int(year),
            value=float(value),
            source_id=source_id,
        )
        session.add(indicator_value)
        existing_indicator_values[value_key] = indicator_value
