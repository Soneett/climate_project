import json
from sqlalchemy.orm import Session
from models import IndicatorValue, Indicator, Region

def load_indicator_values(json_file: str, session: Session, region_id: int):

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    rows = data["indicator_values"]["rows"]

    for row in rows:
        year = row["year"]
        value = row["value"]
        indicator_key = row["indicator_key"]

        indicator = session.query(Indicator).filter_by(name=indicator_key).first()
        if not indicator:
            print(f"Показатель {indicator_key} не найден в indicators, нужно добавить его вручную")
            continue

        iv = IndicatorValue(
            indicator_id=indicator.id,
            region_id=region_id,
            year=year,
            value=value,
            source_id=None
        )
        session.add(iv)

    session.commit()
