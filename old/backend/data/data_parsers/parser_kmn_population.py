#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import re
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


def clean_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and math.isnan(x):
        return ""
    s = str(x).replace("\xa0", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def to_number(x: Any):
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None

    s = clean_text(x)
    if s == "":
        return None

    s = re.sub(r"[^\d,.\-]", "", s)
    s = s.replace(",", ".")

    if s in ("", ".", "-"):
        return None

    try:
        v = float(s)
        if v.is_integer():
            return int(v)
        return v
    except Exception:
        return None


def detect_year_cell(x: Any) -> Optional[int]:
    s = clean_text(x)
    m = re.search(r"\b(19|20)\d{2}\b", s)
    return int(m.group(0)) if m else None


def is_skip_name(name: str) -> bool:
    n = clean_text(name).lower()
    if not n:
        return True
    if n.endswith(":"):
        return True
    if n in ("в том числе:", "в том числе", "муниципальные районы:", "муниципальные районы"):
        return True
    if re.match(r"^\d+\)\s*", n):
        return True
    return False


def find_year_row(df0: pd.DataFrame, max_scan_rows: int = 30) -> Tuple[int, Dict[int, int]]:
    scan = min(max_scan_rows, len(df0))
    for r in range(scan):
        years_here: Dict[int, int] = {}
        for c, val in enumerate(df0.iloc[r].tolist()):
            y = detect_year_cell(val)
            if y is not None:
                years_here[c] = y
        if len(years_here) >= 4:
            return r, years_here
    raise RuntimeError("Не удалось найти строку с годами.")


def normalize_subtype_name(territory: str) -> str:
    t = clean_text(territory)
    low = t.lower()

    if "всего" in low and "республика алтай" in low:
        return "всего"

    if low in ("республика алтай", "республика алтай всего", "всего"):
        return "всего"

    return t


def parse_kmn_population_xlsx(
    xlsx_path: str,
    sheet: int = 0,
    region_name: str = "Республика Алтай",
    indicator_name: str = "Оценка численности населения КМН",
    unit_code: str = "чел",
) -> Dict[str, Any]:

    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    year_row_idx, year_cols = find_year_row(df0)

    rows: List[Dict[str, Any]] = []

    for r in range(year_row_idx + 1, len(df0)):

        territory = clean_text(df0.iloc[r, 0])

        if is_skip_name(territory):
            continue

        any_num = any(to_number(df0.iloc[r, c]) is not None for c in year_cols.keys())
        if not any_num:
            continue

        subtype_name = normalize_subtype_name(territory)

        for c, year in sorted(year_cols.items(), key=lambda x: x[1]):

            v = to_number(df0.iloc[r, c])
            if v is None:
                continue

            rows.append(
                {
                    "region_name": region_name,
                    "year": int(year),
                    "indicator_name": f"{indicator_name} — {subtype_name}",
                    "value": v,
                    "unit_code": unit_code,
                }
            )

    return {
        "meta": {
            "file": xlsx_path,
            "indicator_name": indicator_name,
            "rows_count": len(rows),
        },
        "indicator_values": {
            "rows": rows
        },
    }


if __name__ == "__main__":

    xlsx_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/sources/kmn.xlsx"
    out_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/indicator_values/kmn_population.json"

    result = parse_kmn_population_xlsx(
        xlsx_path=xlsx_path,
        sheet=0,
        region_name="Республика Алтай",
        indicator_name="Оценка численности населения КМН",
        unit_code="чел",
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: сохранено {result['meta']['rows_count']} строк в файл {out_path}")
