from tables.units import UnitsTable

def parse_units(data: list[dict], session):
    def _normalize(value: str | None) -> str:
        return (value or "").strip()

    existing_units = {
        _normalize(u.code): u
        for u in session.query(UnitsTable).all()
    }
    existing_unit_names = {
        _normalize(u.name): u
        for u in session.query(UnitsTable).all()
    }

    for item in data["units"]:
        code = _normalize(item["code"])
        name = _normalize(item["name"])

        if code in existing_units:
            existing_units[code].name = name
            existing_unit_names[name] = existing_units[code]
        elif name in existing_unit_names:
            unit = existing_unit_names[name]
            unit.code = code
            existing_units[code] = unit
        else:
            unit = UnitsTable(code=code, name=name)
            session.add(unit)
            existing_units[code] = unit
            existing_unit_names[name] = unit
