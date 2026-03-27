from tables.indicators import IndicatorsTable
from tables.units import UnitsTable
from tables.indicator_subtypes import IndicatorSubtypesTable

def parse_indicators(data: list[dict], session):
    units_map = {
        u.code: u.id
        for u in session.query(UnitsTable).all()
    }

    subtypes_map = {
        s.name: s.id
        for s in session.query(IndicatorSubtypesTable).all()
    }

    existing_indicators = {ind.name: ind for ind in session.query(IndicatorsTable).all()}

    for item in data["indicators"]:
        name = item["name"]

        values = dict(
            unit_id=units_map.get(item["unit_code"]),
            type=item.get("type"),
            theme=item.get("theme"),
            subtype_id=subtypes_map.get(item["subtype"]),
        )

        if name in existing_indicators:
            indicator = existing_indicators[name]
            for k, v in values.items():
                setattr(indicator, k, v)
        else:
            indicator = IndicatorsTable(name=name, **values)
            session.add(indicator)
            session.flush()
            existing_indicators[name] = indicator
