from tables.regions import RegionsTable

def parse_regions(data: dict, session):
    existing_by_code = {r.code: r for r in session.query(RegionsTable).all()}
    existing_by_name = {r.name: r for r in session.query(RegionsTable).all()}

    for item in data["regions"]:
        code = item["code"]
        name = item["name"]
        by_code = existing_by_code.get(code)
        by_name = existing_by_name.get(name)

        if by_code:
            r = by_code
            r.name = name
            r.type = item.get("type")
            r.parent_id = item.get("parent_id")
            existing_by_name[name] = r
        elif by_name:
            by_name.code = code
            by_name.type = item.get("type")
            by_name.parent_id = item.get("parent_id")
            existing_by_code[code] = by_name
        else:
            region = RegionsTable(
                code=code,
                name=name,
                type=item.get("type"),
                parent_id=item.get("parent_id"),
            )
            session.add(region)
            session.flush()
            existing_by_code[code] = region
            existing_by_name[name] = region


