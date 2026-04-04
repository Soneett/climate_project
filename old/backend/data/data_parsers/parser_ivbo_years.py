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
    s = str(x).replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def to_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x)
    s = clean_text(x)
    if s == "":
        return None
    s = s.replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)
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
    s = clean_text(x)
    m = re.search(r"\b(19|20)\d{2}\b", s)
    if not m:
        return None
    y = int(m.group(0))
    if 1900 <= y <= 2100:
        return y
    return None


def find_year_row_and_cols(df: pd.DataFrame) -> Tuple[int, Dict[int, int]]:
    best_row = None
    best_cols: Dict[int, int] = {}
    max_years = 0

    nrows = min(len(df), 80)
    ncols = min(df.shape[1], 80)

    for r in range(nrows):
        cols: Dict[int, int] = {}
        for c in range(ncols):
            y = detect_year_cell(df.iat[r, c])
            if y is not None:
                cols[c] = y
        if len(cols) >= 2 and len(cols) > max_years:
            best_row = r
            best_cols = cols
            max_years = len(cols)

    if best_row is None:
        raise RuntimeError("Не удалось найти строку с годами.")
    return best_row, best_cols


def guess_title(df: pd.DataFrame, up_to_row: int) -> str:
    for r in range(min(up_to_row + 1, 10)):
        t = clean_text(df.iat[r, 0] if df.shape[1] > 0 else "")
        if t and "к содержанию" not in t.lower():
            return t
    return "Индекс выпуска товаров и услуг"


def parse_ivbo_yearly(
    xlsx_path: str,
    sheet: str = "3",
    region_name_override: Optional[str] = None,
) -> Dict[str, Any]:
    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    year_row_idx, year_cols = find_year_row_and_cols(df0)
    title = guess_title(df0, year_row_idx)

    rows: List[Dict[str, Any]] = []
    nrows = len(df0)

    for r in range(year_row_idx + 1, nrows):
        rn = clean_text(df0.iat[r, 0] if df0.shape[1] > 0 else "")
        if rn == "":
            continue

        values_present = False
        for c in year_cols.keys():
            if c < df0.shape[1] and to_number(df0.iat[r, c]) is not None:
                values_present = True
                break
        if not values_present:
            continue

        region_name = region_name_override or rn

        for c, year in year_cols.items():
            if c >= df0.shape[1]:
                continue
            val = to_number(df0.iat[r, c])
            if val is None:
                continue
            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": title,
                    "value": val,
                    "unit_code": "%",
                }
            )

    out: Dict[str, Any] = {
        "meta": {
            "file": xlsx_path,
            "sheet": sheet,
            "rows_count": len(rows),
            "years_found": sorted({x["year"] for x in rows}),
            "regions_found": sorted({x["region_name"] for x in rows}),
            "indicator_name": title,
            "year_header_row": year_row_idx,
            "year_cols": {str(k): v for k, v in year_cols.items()},
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/IVBO_sub_2024(11).xlsx"
    out_path = "/home/daria/altay-db/ivbo_yearly_altai.json"

    result = parse_ivbo_yearly(xlsx_path, sheet="3", region_name_override=None)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("Regions:", result["meta"]["regions_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
