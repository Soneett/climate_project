from sqlalchemy.orm import Session

from tables.population_age_sex import PopulationAgeSexTable

DEFAULT_SEX_CODE = "A"
DEFAULT_AGE_CODE = "A"


def parse_population_rows(
    rows: list[dict],
    session: Session,
    *,
    region_id: int,
    source_id: int,
):

    for item in rows:
        year = item["year"]
        value = item["value"]

        sex_code = item.get("sex_code", DEFAULT_SEX_CODE)
        age_code = item.get("age_code", DEFAULT_AGE_CODE)

        existing = (
            session.query(PopulationAgeSexTable)
            .filter_by(
                region_id=region_id,
                year=year,
                sex_code=sex_code,
                age_code=age_code,
            )
            .first()
        )

        if existing:
            existing.value = value
            existing.source_id = source_id
            continue

        session.add(
            PopulationAgeSexTable(
                region_id=region_id,
                year=year,
                sex_code=sex_code,
                age_code=age_code,
                value=value,
                source_id=source_id,
            )
        )

    session.commit()
