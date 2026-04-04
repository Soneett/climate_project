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
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s


def to_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, float):
        if math.isnan(x):
            return None
        return float(int(x)) if float(x).is_integer() else float(x)

    s = clean_text(x)
    if s == "":
        return None

    s = s.replace(" ", "")
    s = s.replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)

    if s in ("", ".", "-"):
        return None

    try:
        v = float(s)
        return float(int(v)) if v.is_integer() else v
    except Exception:
        return None


def detect_year_cell(x: Any) -> Optional[int]:
    s = clean_text(x)
    m = re.search(r"\b(19|20)\d{2}\b", s)
    return int(m.group(0)) if m else None


def parse_org_ownership_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:
    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    year_row_idx = None
    year_cols: Dict[int, int] = {}

    for r in range(len(df0)):
        found: Dict[int, int] = {}
        for c in range(df0.shape[1]):
            y = detect_year_cell(df0.iat[r, c])
            if y is not None:
                found[c] = y
        if len(found) >= 2:
            year_row_idx = r
            year_cols = found
            break

    if year_row_idx is None:
        raise RuntimeError("Не удалось найти строку с годами.")

    rows: List[Dict[str, Any]] = []
    unit_code = "единиц"

    for r in range(year_row_idx + 1, len(df0)):
        name_clean = clean_text(df0.iat[r, 0])

        numeric_present = False
        for c in year_cols.keys():
            if to_number(df0.iat[r, c]) is not None:
                numeric_present = True
                break

        if not numeric_present:
            continue

        if name_clean == "":
            continue

        if re.search(r"\bв том числе\b", name_clean.lower()):
            continue

        indicator_name = "Количество организаций — " + name_clean

        for c, year in year_cols.items():
            val = to_number(df0.iat[r, c])
            if val is None:
                continue
            if float(val).is_integer():
                val = int(val)

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
            "years_found": sorted({x["year"] for x in rows}),
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Количество организаций по формам собственности.xlsx"
    out_path = "/home/daria/altay-db/org_ownership_altai.json"

    result = parse_org_ownership_xlsx(
        xlsx_path=xlsx_path,
        region_name="Республика Алтай",
        sheet=0,
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("OK: saved {} rows to {}".format(result["meta"]["rows_count"], out_path))
    print("Years:", result["meta"]["years_found"])
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
