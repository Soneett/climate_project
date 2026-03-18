from __future__ import annotations

from services.parsers.default_excel_parser import DefaultExcelParser


PARSERS = {
    "Рождаемость": DefaultExcelParser,
    "Смертность": DefaultExcelParser,
    "Численность населения": DefaultExcelParser,
}


def get_parser(indicator_name: str):
    parser_cls = PARSERS.get(indicator_name)
    if parser_cls is None:
        parser_cls = DefaultExcelParser
    return parser_cls()
