from tables.indicator_subtypes import IndicatorSubtypesTable

def parse_indicator_subtypes(data: list[dict], session):
    for item in data:
        existing = session.query(IndicatorSubtypesTable).filter_by(name=item["name"]).first()
        if existing:
            continue
        session.add(IndicatorSubtypesTable(name=item["name"]))
    session.commit()

