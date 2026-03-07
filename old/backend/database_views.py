from sqlalchemy import text
from sqlalchemy.engine import Engine


def create_reporting_views(engine: Engine) -> None:
    statements = [
        "DROP VIEW IF EXISTS vw_indicator_values_enriched",
        """
        CREATE VIEW vw_indicator_values_enriched AS
        SELECT
            iv.id,
            iv.region_id,
            r.name AS region_name,
            iv.indicator_id,
            i.name AS indicator_name,
            i.type AS indicator_type,
            i.theme AS indicator_theme,
            i.subtype_id,
            st.name AS indicator_subtype,
            i.unit_id,
            u.code AS unit_code,
            u.name AS unit_name,
            iv.year,
            iv.value,
            iv.source_id,
            ds.name AS source_name,
            ds.organization AS source_organization
        FROM indicator_values iv
        JOIN indicators i ON i.id = iv.indicator_id
        JOIN regions r ON r.id = iv.region_id
        LEFT JOIN indicator_subtypes st ON st.id = i.subtype_id
        LEFT JOIN units u ON u.id = i.unit_id
        LEFT JOIN data_sources ds ON ds.id = iv.source_id
        WHERE iv.is_deleted = FALSE
          AND i.is_deleted = FALSE
          AND r.is_deleted = FALSE
        """,
        "DROP VIEW IF EXISTS vw_population_age_sex_enriched",
        """
        CREATE VIEW vw_population_age_sex_enriched AS
        SELECT
            pas.id,
            pas.region_id,
            r.name AS region_name,
            pas.year,
            pas.age_code,
            pas.sex_code,
            pas.value,
            pas.source_id,
            ds.name AS source_name,
            ds.organization AS source_organization
        FROM population_age_sex pas
        JOIN regions r ON r.id = pas.region_id
        LEFT JOIN data_sources ds ON ds.id = pas.source_id
        WHERE pas.is_deleted = FALSE
          AND r.is_deleted = FALSE
        """,
    ]

    with engine.begin() as conn:
        for statement in statements:
            conn.execute(text(statement))
