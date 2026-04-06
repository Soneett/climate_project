from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any, Callable


def _lazy_parser(module_path: str, function_name: str) -> Callable[[str], dict[str, Any]]:
    def _runner(file_path: str) -> dict[str, Any]:
        module = import_module(module_path)
        parser_fn = getattr(module, function_name)
        return parser_fn(file_path)

    return _runner


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
        parse_fn=_lazy_parser("data.data_parsers.parser_agri_price_indices", "parse_producer_price_index_agri_pdf"),
        source_file="agri_price_indices.json",
    ),
    "birth_rate": ParserConfig(
        key="birth_rate",
        label="Рождаемость, смертность, естественный прирост",
        parse_fn=_lazy_parser("data.data_parsers.parse_births_deaths_natural", "process_births_deaths_natural_local"),
        source_file="birth_abs.json",
    ),
    "consumption_expenses": ParserConfig(
        key="consumption_expenses",
        label="Расходы на потребление домашних хозяйств",
        parse_fn=_lazy_parser("data.data_parsers.parser_consumption_expenses", "parse_consumption_expenses_xlsx"),
        source_file="consumption_expenses.json",
    ),
    "cpi": ParserConfig(
        key="cpi",
        label="Индексы потребительских цен",
        parse_fn=_lazy_parser("data.data_parsers.parser_cpi_pdf", "parse_cpi_pdf"),
        source_file="cpi.json",
    ),
    "credit_debit_structure": ParserConfig(
        key="credit_debit_structure",
        label="Кредитно-дебетная структура доходов и расходов",
        parse_fn=_lazy_parser("data.data_parsers.parser_credit_debit_structure", "parse_credit_debit_structure_pdf"),
        source_file="credit_debit_structure.json",
    ),
    "demo_org": ParserConfig(
        key="demo_org",
        label="Демография организаций",
        parse_fn=_lazy_parser("data.data_parsers.parser_demo_org2_altai", "parse_demo_org2_altai_years"),
        source_file="demo_org.json",
    ),
    "employment_education": ParserConfig(
        key="employment_education",
        label="Занятость населения по уровню образования",
        parse_fn=_lazy_parser("data.data_parsers.parser_employment_education", "parse_employment_education_pdf"),
        source_file="employment_education.json",
    ),
    "healthcare": ParserConfig(
        key="healthcare",
        label="Основные показатели здравоохранения",
        parse_fn=_lazy_parser("data.data_parsers.parser_healthcare", "parse_healthcare_xlsx"),
        source_file="healthcare_indicators.json",
    ),
    "hightech_share_vrp": ParserConfig(
        key="hightech_share_vrp",
        label="Доля высокотехнологичных отраслей в ВРП",
        parse_fn=_lazy_parser("data.data_parsers.parser_hightech_share_vrp", "parse_hightech_share_vrp_xlsx"),
        source_file="hightech_share_vrp.json",
    ),
    "housing_fund_movement": ParserConfig(
        key="housing_fund_movement",
        label="Движение жилищного фонда",
        parse_fn=_lazy_parser("data.data_parsers.parser_housing_fund_movement", "parse_housing_fund_movement_xls"),
        source_file="housing_fund_movement.json",
    ),
    "income_balance": ParserConfig(
        key="income_balance",
        label="Состав и структура денежных доходов и расходов населения",
        parse_fn=_lazy_parser("data.data_parsers.parser_income_balance", "parse_income_balance_xlsx"),
        source_file="structure_of_income.json",
    ),
    "ivbo": ParserConfig(
        key="ivbo",
        label="Индекс выпуска товаров и услуг",
        parse_fn=_lazy_parser("data.data_parsers.parser_ivbo_years", "parse_ivbo_yearly"),
        source_file="IVBO.json",
    ),
    "kmn_population": ParserConfig(
        key="kmn_population",
        label="Оценка численности коренных малочисленных народов",
        parse_fn=_lazy_parser("data.data_parsers.parser_kmn_population", "parse_kmn_population_xlsx"),
        source_file="kmn_population.json",
    ),
    "migration": ParserConfig(
        key="migration",
        label="Общие итоги миграции населения",
        parse_fn=_lazy_parser("data.data_parsers.parser_migration_increment", "parse_migration_increment_xlsx"),
        source_file="migration.json",
    ),
    "morbidity": ParserConfig(
        key="morbidity",
        label="Заболеваемость по основным классам болезней",
        parse_fn=_lazy_parser("data.data_parsers.parser_morbidity", "parse_morbidity_xlsx"),
        source_file="morbidity.json",
    ),
    "mortality_causes": ParserConfig(
        key="mortality_causes",
        label="Причины смертности населения",
        parse_fn=_lazy_parser("data.data_parsers.parse_mortality_causes_rates", "process_mortality_causes_rates_local"),
        source_file="death_causes.json",
    ),
    "org_liquidation": ParserConfig(
        key="org_liquidation",
        label="Коэффициент ликвидации организаций",
        parse_fn=_lazy_parser("data.data_parsers.parser_org_liquidation", "parse_org_liquidation_ra_yearonly"),
        source_file="org_liquidation.json",
    ),
    "org_ownership": ParserConfig(
        key="org_ownership",
        label="Количество организаций по формам собственности",
        parse_fn=_lazy_parser("data.data_parsers.parser_org_ownership", "parse_org_ownership_xlsx"),
        source_file="org_ownership.json",
    ),
    "population_age_sex": ParserConfig(
        key="population_age_sex",
        label="Половозрастная структура населения",
        parse_fn=_lazy_parser("data.data_parsers.parse_population_age_sex", "parse_population_age_sex_file"),
        source_file="separated_age_sex.json",
    ),
    "poverty_level": ParserConfig(
        key="poverty_level",
        label="Население с доходами ниже границы бедности",
        parse_fn=_lazy_parser("data.data_parsers.parser_poverty_level", "parse_poverty_xlsx"),
        source_file="poverty_level.json",
    ),
    "road_press_release": ParserConfig(
        key="road_press_release",
        label="Состояние автомобильных дорог (пресс-релиз)",
        parse_fn=_lazy_parser("data.data_parsers.parser_roads_press_release", "parse_roads_pdf"),
        source_file="road_press_release.json",
    ),
    "temperature_history": ParserConfig(
        key="temperature_history",
        label="История температур (Горно-Алтайск)",
        parse_fn=_lazy_parser("data.data_parsers.parse_gorno_altaysk_temperature_history", "parse_pogodaiklimat_temperature_history"),
        source_file="temperature_gorno_altaysk.json",
    ),
    "vrp": ParserConfig(
        key="vrp",
        label="Валовой региональный продукт",
        parse_fn=_lazy_parser("data.data_parsers.parser_vrp", "parse_vrp_xlsx"),
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
