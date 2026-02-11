from tables.regions import RegionsTable

def parse_regions(data: dict, session):

    existing_regions = {
        r.code: r
        for r in session.query(RegionsTable).all()
    }

    for item in data["regions"]:
        code = item["code"]

        if code in existing_regions:
            r = existing_regions[code]
            r.name = item["name"]
            r.type = item.get("type")
            r.parent_id = item.get("parent_id")
        else:
            session.add(
                RegionsTable(
                    code=code,
                    name=item["name"],
                    type=item.get("type"),
                    parent_id=item.get("parent_id"),
                )
            )


    


