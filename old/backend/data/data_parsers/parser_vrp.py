#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import re
from typing import Any, Dict, List, Optional, Tuple

#import pandas as pd


def clean_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and math.isnan(x):
        return ""
    s = str(x).replace("\xa0", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s


def to_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        v = float(x)
        if v.is_integer():
            return int(v)
        return v

    s = clean_text(x)
    if s == "":
        return None
    if s.strip() in ("-", "—", "–"):
        return None

    s = s.replace(",", ".")
    s = re.sub(r"[^\d\.\-]", "", s)
    if s in ("", ".", "-", "-."):
        return None

    try:
        v = float(s)
        if v.is_integer():
            return int(v)
        return v
    except Exception:
        return None


def detect_year_cell(x: Any) -> Optional[int]:
    if x is None:
        return None

    if isinstance(x, float) and math.isnan(x):
        return None

    if isinstance(x, (int, float)) and not isinstance(x, bool):
        y = int(float(x))
        if 1900 <= y <= 2100:
            return y
        return None

    s = clean_text(x)
    m = re.search(r"(19|20)\d{2}", s)
    if not m:
        return None
    y = int(m.group(0))
    if 1900 <= y <= 2100:
        return y
    return None


def infer_unit_code(indicator_name: str) -> Optional[str]:
    t = clean_text(indicator_name).lower()
    if "процент" in t or "%" in t:
        return "%"
    if "млн" in t and ("руб" in t or "рубл" in t):
        return "млн_руб"
    if "руб" in t or "рубл" in t:
        return "руб"
    return None


def find_year_header_row(df0: pd.DataFrame) -> Tuple[int, Dict[int, int]]:
    best_row = -1
    best_cols: Dict[int, int] = {}

    max_scan = min(len(df0), 120)
    for r in range(max_scan):
        years_here: Dict[int, int] = {}
        row = df0.iloc[r]
        for c, val in enumerate(row):
            y = detect_year_cell(val)
            if y is not None:
                years_here[c] = y

        uniq_years = sorted(set(years_here.values()))
        if len(uniq_years) >= 6:
            if len(uniq_years) > len(set(best_cols.values())):
                best_row = r
                best_cols = years_here

    if best_row == -1:
        raise RuntimeError("Не удалось найти строку с годами.")

    col2year: Dict[int, int] = {}
    for c in sorted(best_cols.keys()):
        y = best_cols[c]
        if 1900 <= y <= 2100:
            col2year[c] = y

    return best_row, col2year


def parse_sheet(df0: pd.DataFrame, region_name: str) -> List[Dict[str, Any]]:
    year_row_idx, year_cols = find_year_header_row(df0)

    rows: List[Dict[str, Any]] = []
    for r in range(year_row_idx + 1, len(df0)):
        name = clean_text(df0.iloc[r, 0])
        if name == "":
            continue

        values_present = False
        for c in year_cols.keys():
            if to_number(df0.iloc[r, c]) is not None:
                values_present = True
                break
        if not values_present:
            continue

        unit_code = infer_unit_code(name)

        for c, year in year_cols.items():
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue
            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": name,
                    "value": val,
                    "unit_code": unit_code,
                }
            )

    return rows


def parse_vrp_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheets_to_try: Optional[List[str]] = None,
) -> Dict[str, Any]:
    xl = pd.ExcelFile(xlsx_path, engine="openpyxl")
    sheet_names = xl.sheet_names

    if sheets_to_try is None:
        sheets_to_try = [s for s in sheet_names if s != "Содержание"]

    all_rows: List[Dict[str, Any]] = []
    meta_sheets: Dict[str, Any] = {}

    for sh in sheets_to_try:
        try:
            df0 = pd.read_excel(xlsx_path, sheet_name=sh, header=None, engine="openpyxl")
            rows = parse_sheet(df0, region_name=region_name)
            all_rows.extend(rows)
            meta_sheets[sh] = {"rows_count": len(rows)}
        except Exception as e:
            meta_sheets[sh] = {"rows_count": 0, "error": str(e)}

    years_found = sorted({r["year"] for r in all_rows})

    return {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(all_rows),
            "years_found": years_found,
            "sheets": meta_sheets,
        },
        "indicator_values": {"rows": all_rows},
    }


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/ВРП_1998-2023(32) (2).xlsx"
    out_path = "/home/daria/altay-db/vrp_1998_2023.json"

    result = parse_vrp_xlsx(
        xlsx_path=xlsx_path,
        region_name="Республика Алтай",
        sheets_to_try=["1", "2", "3"],
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print(json.dumps(result["indicator_values"]["rows"][:8], ensure_ascii=False, indent=2))
