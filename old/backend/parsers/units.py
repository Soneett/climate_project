from tables.units import UnitsTable

def parse_units(data: list[dict], session):
    existing_units = {
        u.code: u
        for u in session.query(UnitsTable).all()
    }

    for item in data:
        code = item["code"]
        name = item["name"]

        if code in existing_units:
            existing_units[code].name = name
        else:
            session.add(UnitsTable(code=code, name=name))

