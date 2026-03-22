from tables.indicators import IndicatorsTable
from tables.units import UnitsTable
from tables.indicator_subtypes import IndicatorSubtypesTable

def parse_indicators(data: list[dict], session):
    def _normalize(value: str | None) -> str:
        return (value or "").strip()

    units_map = {
        _normalize(u.code): u.id
        for u in session.query(UnitsTable).all()
    }

    subtypes_map = {
        _normalize(s.name): s.id
        for s in session.query(IndicatorSubtypesTable).all()
    }

    existing_indicators = {
        _normalize(ind.name): ind
        for ind in session.query(IndicatorsTable).all()
    }

    for item in data["indicators"]:
        name = _normalize(item["name"])

        values = dict(
            unit_id=units_map.get(_normalize(item.get("unit_code"))),
            type=item.get("type"),
            theme=item.get("theme"),
            subtype_id=subtypes_map.get(_normalize(item.get("subtype"))),
        )

        if name in existing_indicators:
            indicator = existing_indicators[name]
            for k, v in values.items():
                setattr(indicator, k, v)
        else:
            session.add(
                IndicatorsTable(
                    name=name,
                    **values
                )
            )
