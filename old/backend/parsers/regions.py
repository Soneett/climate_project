from sqlalchemy.orm import Session
from tables.regions import RegionsTable

def parse_regions(data: dict, session):

    for item in data["regions"]:
        existing = session.execute(
            session.query(RegionsTable).filter_by(code=item["code"])
        ).scalar_one_or_none()

        if existing:
            existing.name = item["name"]
            existing.type = item.get("type")
            existing.parent_id = item.get("parent_id")  
        else:
            region = RegionsTable(
                name=item["name"],
                code=item.get("code"),
                type=item.get("type"),
                parent_id=item.get("parent_id"),
            )
            session.add(region)
    session.commit()

from sqlalchemy.orm import Session
from tables.regions import RegionsTable

def parse_regions(data: dict, session: Session):
    for item in data["regions"]:
        region = (
            session.query(RegionsTable)
            .filter_by(code=item["code"])
            .one_or_none()
        )

        if region:
            region.name = item["name"]
            region.type = item.get("type")
            region.parent_id = item.get("parent_id")
        else:
            session.add(
                RegionsTable(
                    name=item["name"],
                    code=item["code"],
                    type=item.get("type"),
                    parent_id=item.get("parent_id"),
                )
            )




