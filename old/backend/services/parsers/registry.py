from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from data.data_parsers.parse_births_deaths_natural import process_births_deaths_natural_local
from data.data_parsers.parse_gorno_altaysk_temperature_history import parse_pogodaiklimat_temperature_history
from data.data_parsers.parse_mortality_causes_rates import process_mortality_causes_rates_local
from data.data_parsers.parse_population_age_sex import parse_population_age_sex_file
from data.data_parsers.parser_agri_price_indices import parse_producer_price_index_agri_pdf
from data.data_parsers.parser_consumption_expenses import parse_consumption_expenses_xlsx
from data.data_parsers.parser_cpi_pdf import parse_cpi_pdf
from data.data_parsers.parser_credit_debit_structure import parse_credit_debit_structure_pdf
from data.data_parsers.parser_demo_org2_altai import parse_demo_org2_altai_years
from data.data_parsers.parser_employment_education import parse_employment_education_pdf
from data.data_parsers.parser_healthcare import parse_healthcare_xlsx
from data.data_parsers.parser_hightech_share_vrp import parse_hightech_share_vrp_xlsx
from data.data_parsers.parser_housing_fund_movement import parse_housing_fund_movement_xls
from data.data_parsers.parser_income_balance import parse_income_balance_xlsx
from data.data_parsers.parser_ivbo_years import parse_ivbo_yearly
from data.data_parsers.parser_kmn_population import parse_kmn_population_xlsx
from data.data_parsers.parser_migration_increment import parse_migration_increment_xlsx
from data.data_parsers.parser_morbidity import parse_morbidity_xlsx
from data.data_parsers.parser_org_liquidation import parse_org_liquidation_ra_yearonly
from data.data_parsers.parser_org_ownership import parse_org_ownership_xlsx
from data.data_parsers.parser_poverty_level import parse_poverty_xlsx
from data.data_parsers.parser_roads_press_release import parse_roads_pdf
from data.data_parsers.parser_vrp import parse_vrp_xlsx


@dataclass(frozen=True)
class ParserConfig:
    key: str
    label: str
    parse_fn: Callable[[str], dict[str, Any]]
    source_file: str


_PARSER_CONFIGS: dict[str, ParserConfig] = {
    "agri_price_indices": ParserConfig(
        key="agri_price_indices",
        label="Индексы цен производителей сельхозпродукции",
        parse_fn=parse_producer_price_index_agri_pdf,
        source_file="agri_price_indices.json",
    ),
    "birth_rate": ParserConfig(
        key="birth_rate",
        label="Рождаемость, смертность, естественный прирост",
        parse_fn=process_births_deaths_natural_local,
        source_file="birth_abs.json",
    ),
    "consumption_expenses": ParserConfig(
        key="consumption_expenses",
        label="Расходы на потребление домашних хозяйств",
        parse_fn=parse_consumption_expenses_xlsx,
        source_file="consumption_expenses.json",
    ),
    "cpi": ParserConfig(
        key="cpi",
        label="Индексы потребительских цен",
        parse_fn=parse_cpi_pdf,
        source_file="cpi.json",
    ),
    "credit_debit_structure": ParserConfig(
        key="credit_debit_structure",
        label="Кредитно-дебетная структура доходов и расходов",
        parse_fn=parse_credit_debit_structure_pdf,
        source_file="credit_debit_structure.json",
    ),
    "demo_org": ParserConfig(
        key="demo_org",
        label="Демография организаций",
        parse_fn=parse_demo_org2_altai_years,
        source_file="demo_org.json",
    ),
    "employment_education": ParserConfig(
        key="employment_education",
        label="Занятость населения по уровню образования",
        parse_fn=parse_employment_education_pdf,
        source_file="employment_education.json",
    ),
    "healthcare": ParserConfig(
        key="healthcare",
        label="Основные показатели здравоохранения",
        parse_fn=parse_healthcare_xlsx,
        source_file="healthcare_indicators.json",
    ),
    "hightech_share_vrp": ParserConfig(
        key="hightech_share_vrp",
        label="Доля высокотехнологичных отраслей в ВРП",
        parse_fn=parse_hightech_share_vrp_xlsx,
        source_file="hightech_share_vrp.json",
    ),
    "housing_fund_movement": ParserConfig(
        key="housing_fund_movement",
        label="Движение жилищного фонда",
        parse_fn=parse_housing_fund_movement_xls,
        source_file="housing_fund_movement.json",
    ),
    "income_balance": ParserConfig(
        key="income_balance",
        label="Состав и структура денежных доходов и расходов населения",
        parse_fn=parse_income_balance_xlsx,
        source_file="structure_of_income.json",
    ),
    "ivbo": ParserConfig(
        key="ivbo",
        label="Индекс выпуска товаров и услуг",
        parse_fn=parse_ivbo_yearly,
        source_file="IVBO.json",
    ),
    "kmn_population": ParserConfig(
        key="kmn_population",
        label="Оценка численности коренных малочисленных народов",
        parse_fn=parse_kmn_population_xlsx,
        source_file="kmn_population.json",
    ),
    "migration": ParserConfig(
        key="migration",
        label="Общие итоги миграции населения",
        parse_fn=parse_migration_increment_xlsx,
        source_file="migration.json",
    ),
    "morbidity": ParserConfig(
        key="morbidity",
        label="Заболеваемость по основным классам болезней",
        parse_fn=parse_morbidity_xlsx,
        source_file="morbidity.json",
    ),
    "mortality_causes": ParserConfig(
        key="mortality_causes",
        label="Причины смертности населения",
        parse_fn=process_mortality_causes_rates_local,
        source_file="death_causes.json",
    ),
    "org_liquidation": ParserConfig(
        key="org_liquidation",
        label="Коэффициент ликвидации организаций",
        parse_fn=parse_org_liquidation_ra_yearonly,
        source_file="org_liquidation.json",
    ),
    "org_ownership": ParserConfig(
        key="org_ownership",
        label="Количество организаций по формам собственности",
        parse_fn=parse_org_ownership_xlsx,
        source_file="org_ownership.json",
    ),
    "population_age_sex": ParserConfig(
        key="population_age_sex",
        label="Половозрастная структура населения",
        parse_fn=parse_population_age_sex_file,
        source_file="separated_age_sex.json",
    ),
    "poverty_level": ParserConfig(
        key="poverty_level",
        label="Население с доходами ниже границы бедности",
        parse_fn=parse_poverty_xlsx,
        source_file="poverty_level.json",
    ),
    "road_press_release": ParserConfig(
        key="road_press_release",
        label="Состояние автомобильных дорог (пресс-релиз)",
        parse_fn=parse_roads_pdf,
        source_file="road_press_release.json",
    ),
    "temperature_history": ParserConfig(
        key="temperature_history",
        label="История температур (Горно-Алтайск)",
        parse_fn=parse_pogodaiklimat_temperature_history,
        source_file="temperature_gorno_altaysk.json",
    ),
    "vrp": ParserConfig(
        key="vrp",
        label="Валовой региональный продукт",
        parse_fn=parse_vrp_xlsx,
        source_file="vrp.json",
    ),
}


def get_parser_config(indicator_key: str) -> ParserConfig | None:
    return _PARSER_CONFIGS.get((indicator_key or "").strip().lower())


def list_parser_configs() -> list[dict[str, str]]:
    return [
        {"key": parser.key, "label": parser.label}
        for parser in _PARSER_CONFIGS.values()
    ]
