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
    if not rows:
        return

    existing = {
        (p.year, p.age, p.sex): p
        for p in session.query(PopulationAgeSexTable)
        .filter_by(region_id=region_id)
        .all()
    }

    for row in rows:
        year = row["year"]
        sex_code = row.get("sex_code", DEFAULT_SEX_CODE)
        age_code = row.get("age_code", DEFAULT_AGE_CODE)
        value = row["value"]

        key = (year, age_code, sex_code)

        if key in existing:
            existing[key].value = value
            existing[key].source_id = source_id
        else:
            session.add(
                PopulationAgeSexTable(
                    region_id=region_id,
                    source_id=source_id,
                    year=year,
                    sex_code=sex_code,
                    age_code=age_code,
                    value=value,
                )
            )


