from tables.units import UnitsTable

def parse_units(data: list[dict], session):
    existing_by_code = {u.code: u for u in session.query(UnitsTable).all()}
    existing_by_name = {u.name: u for u in session.query(UnitsTable).all()}

    for item in data["units"]:
        code = item["code"]
        name = item["name"]

        by_code = existing_by_code.get(code)
        by_name = existing_by_name.get(name)

        if by_code:
            by_code.name = name
            existing_by_name[name] = by_code
        elif by_name:
            by_name.code = code
            existing_by_code[code] = by_name
        else:
            unit = UnitsTable(code=code, name=name)
            session.add(unit)
            session.flush()
            existing_by_code[code] = unit
            existing_by_name[name] = unit
