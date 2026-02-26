from sqlalchemy.orm import Session
from tables.indicator_values import IndicatorValuesTable
from tables.indicator_subtypes import IndicatorSubtypesTable
from tables.indicators import IndicatorsTable
from tables.regions import RegionsTable
from tables.data_sources import DataSourcesTable
from tables.units import UnitsTable

def parse_indicator_values(data: dict, session: Session):

    metadata = data.get("metadata", {})
    region_name = metadata.get("region_name")
    source_name = metadata.get("source_name")

    rows = data.get("indicator_values", {}).get("rows", [])
    if not rows:
        return

    regions_map = {
        r.name.strip(): r.id
        for r in session.query(RegionsTable).all()
    }

    sources_map = {
        s.name.strip(): s.id
        for s in session.query(DataSourcesTable).all()
    }

    indicators_map = {
        i.name.strip(): i
        for i in session.query(IndicatorsTable).all()
    }

    subtypes_map = {
        s.name.strip(): s.id
        for s in session.query(IndicatorSubtypesTable).all()
    }

    units_map = {
        u.code.strip(): u.id
        for u in session.query(UnitsTable).all()
    }


    INDICATOR_KEY_MAP = {
        "births_abs": ("Рождаемость", None),
        "mortality_abs": ("Смертность", None),
        "infant_mortality_abs": ("Смертность", "до 1 года"),
    }


    for row in rows:

        row_region = row.get("region_name") or region_name
        if not row_region:
            continue

        row_region = row_region.replace("-всего", "").strip()

        region_id = regions_map.get(row_region)
        if not region_id:
            continue

        source_id = sources_map.get(source_name)
        if not source_id:
            continue

        indicator_name = None
        subtype_id = None

        if "indicator_key" in row:
            key = row["indicator_key"]

            if key not in INDICATOR_KEY_MAP:
                continue

            indicator_name, subtype_name = INDICATOR_KEY_MAP[key]

            indicator = indicators_map.get(indicator_name)
            if not indicator:
                continue

            if subtype_name:
                subtype_id = subtypes_map.get(subtype_name)

        elif "indicator_name" in row:
            full_name = row["indicator_name"].strip()

            if "—" in full_name:
                base, subtype = full_name.split("—", 1)
                indicator_name = base.strip()
                subtype_name = subtype.split(",")[0].strip()
            else:
                indicator_name = full_name
                subtype_name = None

            indicator = indicators_map.get(indicator_name)
            if not indicator:
                continue

            if subtype_name:
                subtype_id = subtypes_map.get(subtype_name)

        else:
            continue

        unit_id = None
        if "unit_code" in row:
            unit_id = units_map.get(row["unit_code"])

        session.add(
            IndicatorValuesTable(
                region_id=region_id,
                indicator_id=indicator.id,
                subtype_id=subtype_id,
                year=row["year"],
                value=row["value"],
                source_id=source_id,
                unit_id=unit_id,
            )
        )
