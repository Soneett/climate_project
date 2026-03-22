from tables.indicator_subtypes import IndicatorSubtypesTable

def parse_indicator_subtypes(data: list[dict], session):
    def _normalize(value: str | None) -> str:
        return (value or "").strip()

    existing = {
        _normalize(s.name): s
        for s in session.query(IndicatorSubtypesTable).all()
    }

    for item in data["indicator_subtypes"]:
        name = _normalize(item["name"])

        if name not in existing:
            session.add(IndicatorSubtypesTable(name=name))
