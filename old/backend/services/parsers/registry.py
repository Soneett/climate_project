from __future__ import annotations

import importlib.util
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

from services.parsers.default_excel_parser import DefaultExcelParser
from services.parsers.indicator_function_parser import IndicatorFunctionParser


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PARSERS_DIR = BASE_DIR / "data" / "data_parsers"


def _normalize_indicator(indicator_name: str) -> str:
    return (indicator_name or "").strip().lower().replace("-", "_").replace(" ", "_")


@lru_cache(maxsize=None)
def _load_parser_function(module_filename: str, function_name: str) -> Callable[..., dict[str, Any]]:
    module_path = DATA_PARSERS_DIR / module_filename
    if not module_path.exists():
        raise RuntimeError(f"Parser module not found: {module_path}")

    module_name = f"data_parser_{module_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load parser module: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    parse_function = getattr(module, function_name, None)
    if not callable(parse_function):
        raise RuntimeError(f"Function {function_name} was not found in {module_path}")

    return parse_function


PARSERS: dict[str, dict[str, str]] = {
    "vrp": {"module": "parser_vrp.py", "function": "parse_vrp_xlsx", "source_file": "vrp"},
    "валовой_региональный_продукт": {"module": "parser_vrp.py", "function": "parse_vrp_xlsx", "source_file": "vrp"},
    "migration": {
        "module": "parser_migration_increment.py",
        "function": "parse_migration_increment_xlsx",
        "source_file": "migration",
    },
    "migration_increment": {
        "module": "parser_migration_increment.py",
        "function": "parse_migration_increment_xlsx",
        "source_file": "migration",
    },
    "миграция": {
        "module": "parser_migration_increment.py",
        "function": "parse_migration_increment_xlsx",
        "source_file": "migration",
    },
    "poverty_level": {
        "module": "parser_poverty_level.py",
        "function": "parse_poverty_xlsx",
        "source_file": "poverty_level",
    },
    "бедность": {"module": "parser_poverty_level.py", "function": "parse_poverty_xlsx", "source_file": "poverty_level"},
}


def get_parser(indicator_name: str):
    parser_config = PARSERS.get(_normalize_indicator(indicator_name))
    if parser_config is None:
        return DefaultExcelParser()

    parse_function = _load_parser_function(parser_config["module"], parser_config["function"])
    return IndicatorFunctionParser(
        parse_function=parse_function,
        parser_name=parser_config["function"],
        source_file=parser_config["source_file"],
    )
