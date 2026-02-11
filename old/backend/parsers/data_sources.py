from tables.data_sources import DataSourcesTable

def parse_data_sources(data: list[dict], session):
    existing = {
        ds.name: ds
        for ds in session.query(DataSourcesTable).all()
    }

    for item in data["data_sources"]:
        name = item["name"]

        if name in existing:
            ds = existing[name]
            ds.url = item.get("url")
            ds.organization = item.get("organization")
            ds.date_collected = item.get("date_collected")
        else:
            session.add(
                DataSourcesTable(
                    name=name,
                    url=item.get("url"),
                    organization=item.get("organization"),
                    date_collected=item.get("date_collected")
                )
            )

