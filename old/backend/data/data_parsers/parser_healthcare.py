#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import re

from typing import Any, Dict, List

import pandas as pd

# утилиты

def clean_text(x: Any) -> str:
    """Нормализация текста - убираем неразрывные пробелы, лишние пробелы"""
    if x is None:
        return ""
    if isinstance(x, float) and math.isnan(x):
        return ""
    s = str(x).replace("\xa0", " ")
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def to_number(x: Any):
    """ячейка в число"""
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    s = clean_text(x)
    if s == "":
        return None

    # оставить только цифры, знаки и разделители
    s = re.sub(r"[^\d,.\-]", "", s)
    s = s.replace(",", ".")
    if s in ("", ".", "-"):
        return None

    try:
        v = float(s)
        return int(v) if isinstance(v, float) and v.is_integer() else v
    except Exception:
        return None


def detect_year_cell(x: Any):
    """Если в ячейке есть год (2017, 2020 и т.п.) - вернём его как int, иначе None."""
    s = clean_text(x)
    m = re.search(r"(19|20)\d{2}", s)
    return int(m.group(0)) if m else None


def infer_unit_from_text(group_text: str, row_text: str) -> str:
    t = (clean_text(group_text) + " " + clean_text(row_text)).lower()

    if "на 10 000" in t or "на 10000" in t:
        if "детей" in t:
            return "на_10000_детей"
        return "на_10000_нас"

    if "на 1 000" in t or "на 1000" in t:
        return "на_1000_нас"

    if "посещени" in t:
        return "посещений_в_смену"

    if "человек" in t or "населен" in t:
        return "чел"

    if "коек" in t or "койко" in t:
        return "коек"

    if "единиц" in t or "единицы" in t:
        return "единиц"

    return None


# основной парсер 

def parse_healthcare_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:

    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    # 1) Ищем строку, где стоят годы (2017, 2018, 2019, ...).
    year_row_idx = None
    year_cols: Dict[int, int] = {}

    for r in range(len(df0)):
        years_here: Dict[int, int] = {}
        row_values = df0.iloc[r]
        for c, val in enumerate(row_values):
            y = detect_year_cell(val)
            if y is not None:
                years_here[c] = y
        # если в строке нашли хотя бы 2 года — считаем её строкой заголовка лет
        if len(years_here) >= 2:
            year_row_idx = r
            year_cols = years_here
            break

    if year_row_idx is None:
        raise RuntimeError("Не удалось найти строку с годами (2017, 2018, ...).")

    # 2) Идём ниже по строкам — там показатели
    rows: List[Dict[str, Any]] = []
    current_group: str | None = None  # например: "Численность врачей всех специальностей"

    for r in range(year_row_idx + 1, len(df0)):
        raw0 = df0.iloc[r, 0]             # текст в первом столбце
        name_clean = clean_text(raw0)     # очищенное имя строки

        # есть ли хоть одно число в столбцах с годами?
        numeric_present = any(
            to_number(df0.iloc[r, c]) is not None for c in year_cols.keys()
        )

        # a) строка без чисел - это либо группа, либо пустота/сноска
        if not numeric_present:
            if name_clean:
                current_group = name_clean
            continue

        # b) строка с числами, но без названия — пропускаем
        if not name_clean:
            continue

        # c) решаем, это подстрока (всего/на 10 000) или самостоятельный показатель
        #    подстрока: "всего, ...", "на 10 000 ..." и т.п., при этом есть current_group
        is_subrow = bool(
            re.search(r"\bвсего\b|\bна 10 000\b|\bна 10000\b", name_clean)
        ) and current_group is not None

        if is_subrow:
            indicator_name = f"{current_group}"
            unit_code = infer_unit_from_text(current_group, name_clean)
        else:
            indicator_name = name_clean
            unit_code = infer_unit_from_text("", name_clean)

        # d) раскладываем по годам
        for c, year in year_cols.items():
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue

            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": indicator_name,
                    "value": val,
                    "unit_code": unit_code,
                }
            )

    out: Dict[str, Any] = {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
            "indicators_found": sorted({r["indicator_name"] for r in rows}),
            "year_header_row": year_row_idx,
            "year_cols": year_cols,
        },
        "indicator_values": {
            "rows": rows
        },
    }
    return out


# запуск из консоли 

if __name__ == "__main__":
    xlsx_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/healthcare.xlsx"
    out_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/indicator_values/healthcare.json"

    result = parse_healthcare_xlsx(
        xlsx_path,
        region_name="Республика Алтай",
        sheet=0,
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
