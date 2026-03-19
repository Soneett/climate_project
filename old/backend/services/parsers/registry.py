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
    parse_fn: Callable[[str], dict[str, Any]]
    source_file: str


_PARSER_CONFIGS: dict[str, ParserConfig] = {
    "демографические показатели: рождаемость, смертность, естественный прирост": ParserConfig(
        parse_fn=process_births_deaths_natural_local,
        source_file="birth_abs.json",
    ),
    "общие итоги миграции населения": ParserConfig(
        parse_fn=parse_migration_increment_xlsx,
        source_file="migration.json",
    ),
    "население с денежными доходами ниже границы бедности": ParserConfig(
        parse_fn=parse_poverty_xlsx,
        source_file="poverty_level.json",
    ),
    "основные показатели здравоохранения": ParserConfig(
        parse_fn=parse_healthcare_xlsx,
        source_file="healthcare_indicators.json",
    ),
    "валовой региональный продукт": ParserConfig(
        parse_fn=parse_vrp_xlsx,
        source_file="vrp.json",
    ),
    "индекс выпуска товаров и услуг по базовым видам экономической деятельности": ParserConfig(
        parse_fn=parse_ivbo_yearly,
        source_file="IVBO.json",
    ),
    "расходы на потребление домашних хозяйств": ParserConfig(
        parse_fn=parse_consumption_expenses_xlsx,
        source_file="consumption_expenses.json",
    ),
    "движение жилищного фонда": ParserConfig(
        parse_fn=parse_housing_fund_movement_xls,
        source_file="housing_fund_movement.json",
    ),
    "количество организаций по формам собственности": ParserConfig(
        parse_fn=parse_org_ownership_xlsx,
        source_file="org_ownership.json",
    ),
    "коэффициент ликвидации организаций": ParserConfig(
        parse_fn=parse_org_liquidation_ra_yearonly,
        source_file="org_liquidation.json",
    ),
    "оценка численности коренных малочисленных народов": ParserConfig(
        parse_fn=parse_kmn_population_xlsx,
        source_file="kmn_population.json",
    ),
    "vrp": ParserConfig(parse_fn=parse_vrp_xlsx, source_file="vrp.json"),
    "poverty_level": ParserConfig(parse_fn=parse_poverty_xlsx, source_file="poverty_level.json"),
    "healthcare": ParserConfig(parse_fn=parse_healthcare_xlsx, source_file="healthcare_indicators.json"),
    "ivbo": ParserConfig(parse_fn=parse_ivbo_yearly, source_file="IVBO.json"),
    "migration": ParserConfig(parse_fn=parse_migration_increment_xlsx, source_file="migration.json"),
    "consumption_expenses": ParserConfig(
        parse_fn=parse_consumption_expenses_xlsx,
        source_file="consumption_expenses.json",
    ),
}


def _normalize_indicator_name(indicator_name: str) -> str:
    return indicator_name.strip().lower()


def get_parser_config(indicator_name: str) -> ParserConfig | None:
    return _PARSER_CONFIGS.get(_normalize_indicator_name(indicator_name))