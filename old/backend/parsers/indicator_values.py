from sqlalchemy.orm import Session
from tables.indicator_values import IndicatorValuesTable
from tables.indicators import IndicatorsTable


def parse_indicator_values(
    rows: list[dict],
    session: Session,
    *,
    region_id: int,
    source_id: int,
):
    if not rows:
        return

    indicators_map = {
        i.key: i.id
        for i in session.query(IndicatorsTable).all()
    }

    existing = {
        (v.indicator_id, v.year): v
        for v in session.query(IndicatorValuesTable)
        .filter_by(region_id=region_id)
        .all()
    }

    for row in rows:
        indicator_key = row["indicator_key"]
        indicator_id = indicators_map.get(indicator_key)

        if not indicator_id:
            continue

        year = row["year"]
        value = row["value"]

        key = (indicator_id, year)

        if key in existing:
            existing[key].value = value
            existing[key].source_id = source_id
        else:
            session.add(
                IndicatorValuesTable(
                    indicator_id=indicator_id,
                    region_id=region_id,
                    source_id=source_id,
                    year=year,
                    value=value,
                )
            )







