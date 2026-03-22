from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from data.data_parsers.parse_births_deaths_natural import process_births_deaths_natural_local
from data.data_parsers.parser_consumption_expenses import parse_consumption_expenses_xlsx
from data.data_parsers.parser_healthcare import parse_healthcare_xlsx
from data.data_parsers.parser_housing_fund_movement import parse_housing_fund_movement_xls
from data.data_parsers.parser_ivbo_years import parse_ivbo_yearly
from data.data_parsers.parser_kmn_population import parse_kmn_population_xlsx
from data.data_parsers.parser_migration_increment import parse_migration_increment_xlsx
from data.data_parsers.parser_org_liquidation import parse_org_liquidation_ra_yearonly
from data.data_parsers.parser_org_ownership import parse_org_ownership_xlsx
from data.data_parsers.parser_poverty_level import parse_poverty_xlsx
from data.data_parsers.parser_vrp import parse_vrp_xlsx


@dataclass(frozen=True)
class ParserConfig:
    key: str
    label: str
    parse_fn: Callable[[str], dict[str, Any]]
    source_file: str


_PARSER_CONFIGS: dict[str, ParserConfig] = {
    "births_deaths_natural": ParserConfig(
        key="births_deaths_natural",
        label="Демографические показатели: рождаемость, смертность, естественный прирост",
        parse_fn=process_births_deaths_natural_local,
        source_file="birth_abs.json",
    ),
    "migration": ParserConfig(
        key="migration",
        label="Общие итоги миграции населения",
        parse_fn=parse_migration_increment_xlsx,
        source_file="migration.json",
    ),
    "poverty_level": ParserConfig(
        key="poverty_level",
        label="Население с денежными доходами ниже границы бедности",
        parse_fn=parse_poverty_xlsx,
        source_file="poverty_level.json",
    ),
    "healthcare_indicators": ParserConfig(
        key="healthcare_indicators",
        label="Основные показатели здравоохранения",
        parse_fn=parse_healthcare_xlsx,
        source_file="healthcare_indicators.json",
    ),
    "vrp": ParserConfig(
        key="vrp",
        label="Валовой региональный продукт",
        parse_fn=parse_vrp_xlsx,
        source_file="vrp.json",
    ),
    "ivbo": ParserConfig(
        key="ivbo",
        label="Индекс выпуска товаров и услуг по базовым видам экономической деятельности",
        parse_fn=parse_ivbo_yearly,
        source_file="IVBO.json",
    ),
    "consumption_expenses": ParserConfig(
        key="consumption_expenses",
        label="Расходы на потребление домашних хозяйств",
        parse_fn=parse_consumption_expenses_xlsx,
        source_file="consumption_expenses.json",
    ),
    "housing_fund_movement": ParserConfig(
        key="housing_fund_movement",
        label="Движение жилищного фонда",
        parse_fn=parse_housing_fund_movement_xls,
        source_file="housing_fund_movement.json",
    ),
    "org_ownership": ParserConfig(
        key="org_ownership",
        label="Количество организаций по формам собственности",
        parse_fn=parse_org_ownership_xlsx,
        source_file="org_ownership.json",
    ),
    "org_liquidation": ParserConfig(
        key="org_liquidation",
        label="Коэффициент ликвидации организаций",
        parse_fn=parse_org_liquidation_ra_yearonly,
        source_file="org_liquidation.json",
    ),
    "kmn_population": ParserConfig(
        key="kmn_population",
        label="Оценка численности коренных малочисленных народов",
        parse_fn=parse_kmn_population_xlsx,
        source_file="kmn_population.json",
    ),
}


_ALIASES_TO_KEYS: dict[str, str] = {
    "демографические показатели: рождаемость, смертность, естественный прирост": "births_deaths_natural",
    "общие итоги миграции населения": "migration",
    "население с денежными доходами ниже границы бедности": "poverty_level",
    "основные показатели здравоохранения": "healthcare_indicators",
    "валовой региональный продукт": "vrp",
    "индекс выпуска товаров и услуг по базовым видам экономической деятельности": "ivbo",
    "расходы на потребление домашних хозяйств": "consumption_expenses",
    "движение жилищного фонда": "housing_fund_movement",
    "количество организаций по формам собственности": "org_ownership",
    "коэффициент ликвидации организаций": "org_liquidation",
    "оценка численности коренных малочисленных народов": "kmn_population",
    "healthcare": "healthcare_indicators",
}


def _normalize(value: str) -> str:
    return value.strip().lower()


def get_parser_config(indicator_key: str) -> ParserConfig | None:
    normalized = _normalize(indicator_key)
    parser_key = _ALIASES_TO_KEYS.get(normalized, normalized)
    return _PARSER_CONFIGS.get(parser_key)


def list_parser_options() -> list[dict[str, str]]:
    return [
        {"key": parser.key, "label": parser.label}
        for parser in _PARSER_CONFIGS.values()
    ]
