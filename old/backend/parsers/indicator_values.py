from sqlalchemy.orm import Session

from tables.indicators import IndicatorsTable
from tables.indicator_values import IndicatorValuesTable

INDICATOR_KEY_TO_NAME = {
    "births_abs": "Рождаемость",
    "deaths_abs": "Смертность",
    "infant_deaths_abs": "Смертность (до 1 года)"
}

def parse_indicator_values(
    data: list[dict],
    session: Session,
    *,
    region_id: int,
    source_id: int,
):

    indicators_map = {
        i.name: i.id
        for i in session.query(IndicatorsTable).all()
    }

    for item in data:
        indicator_key = item["indicator_key"]
        indicator_name = INDICATOR_KEY_TO_NAME.get(indicator_key)

        if indicator_name is None:
            continue

        indicator_id = indicators_map.get(indicator_name)
        if indicator_id is None:
            continue

        year = item["year"]

        existing = (
            session.query(IndicatorValuesTable)
            .filter_by(
                indicator_id=indicator_id,
                region_id=region_id,
                year=year,
            )
            .first()
        )

        if existing:
            existing.value = item["value"]
            existing.source_id = source_id
            continue

        session.add(
            IndicatorValuesTable(
                indicator_id=indicator_id,
                region_id=region_id,
                source_id=source_id,
                year=year,
                value=item["value"],
            )
        )

    session.commit()






