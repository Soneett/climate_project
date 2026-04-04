#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import re
from typing import Any, Dict, List, Optional

#import pandas as pd


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
    s = clean_text(x)
    if not s:
        return None
    s = s.replace("—", "").replace("–", "").replace("−", "")
    s = s.replace(" ", "").replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)
    if s in ("", ".", "-", "-.", ".-"):
        return None
    try:
        v = float(s)
        if v.is_integer():
            return int(v)
        return v
    except Exception:
        return None


def normalize_unit(unit_text: str) -> Optional[str]:
    t = clean_text(unit_text).lower()

    if not t:
        return None

    if "тысяч" in t and "человек" in t:
        return "тыс_чел"

    if "млн" in t and ("руб" in t or "рубл" in t):
        if "в месяц" in t or "в мес" in t:
            return "млн_руб_мес"
        return "млн_руб"

    if "процент" in t or "в процентах" in t or "%" in t:
        return "%"

    return clean_text(unit_text)


def parse_poverty_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:
    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    header_row_idx = None
    for r in range(min(20, len(df0))):
        if clean_text(df0.iloc[r, 0]).lower() == "год":
            header_row_idx = r
            break
    if header_row_idx is None:
        raise RuntimeError("Не найдена строка заголовка, где в первом столбце написано 'Год'.")

    unit_row_idx = header_row_idx + 1
    if unit_row_idx >= len(df0):
        raise RuntimeError("Не найдена строка с единицами измерения (следующая после заголовка).")

    ncols = df0.shape[1]
    top = [clean_text(df0.iloc[header_row_idx, c]) for c in range(ncols)]
    sub = [clean_text(df0.iloc[unit_row_idx, c]) for c in range(ncols)]

    top_ffill: List[str] = []
    last = ""
    for c in range(ncols):
        if top[c]:
            last = top[c]
        top_ffill.append(last)

    indicators: Dict[int, Dict[str, Any]] = {}
    for c in range(1, ncols):
        top_name = top_ffill[c]
        sub_name = sub[c]
        if not top_name and not sub_name:
            continue
        if top_name.lower() == "год":
            continue
        ind_name = top_name
        if sub_name and sub_name.lower() not in ("год",):
            ind_name = (top_name + " — " + sub_name).strip(" —")
        unit_code = normalize_unit(sub_name)
        indicators[c] = {"indicator_name": ind_name, "unit_code": unit_code}

    rows: List[Dict[str, Any]] = []
    years: List[int] = []

    for r in range(unit_row_idx + 1, len(df0)):
        year_val = to_number(df0.iloc[r, 0])
        if year_val is None:
            continue
        year_int = int(year_val)
        if year_int < 1900 or year_int > 2100:
            continue
        years.append(year_int)

        for c, meta in indicators.items():
            v = to_number(df0.iloc[r, c])
            if v is None:
                continue
            rows.append(
                {
                    "region_name": region_name,
                    "year": year_int,
                    "indicator_name": meta["indicator_name"],
                    "value": v,
                    "unit_code": meta["unit_code"],
                }
            )

    out: Dict[str, Any] = {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted(set(years)),
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Численность населения Республики Алтай с денежными доходами ниже границы бедности(2).xlsx"
    out_path = "/home/daria/altay-db/poverty_altai.json"

    result = parse_poverty_xlsx(xlsx_path, region_name="Республика Алтай", sheet=0)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
