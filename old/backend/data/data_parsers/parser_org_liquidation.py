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


def to_number(x: Any):
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    if isinstance(x, (int, float)):
        if isinstance(x, float) and x.is_integer():
            return int(x)
        return x
    s = clean_text(x)
    if s == "":
        return None
    s = re.sub(r"[^\d,.\-]", "", s).replace(",", ".")
    if s in ("", ".", "-"):
        return None
    try:
        v = float(s)
        if v.is_integer():
            return int(v)
        return v
    except Exception:
        return None


def find_year_col(df: pd.DataFrame) -> Tuple[Optional[int], Optional[int]]:
    max_rows = min(80, len(df))
    max_cols = min(60, df.shape[1])
    for r in range(max_rows):
        for c in range(max_cols):
            v = clean_text(df.iat[r, c]).lower()
            if v == "за год" or "за год" in v:
                return r, c
    return None, None


def find_row_by_firstcol(df: pd.DataFrame, target: str, start_row: int) -> Optional[int]:
    t = clean_text(target).lower()
    for r in range(start_row, len(df)):
        v = clean_text(df.iat[r, 0]).lower()
        if v == t:
            return r
    return None


def normalize_indicator_title(raw: str) -> str:
    s = clean_text(raw)
    s = s.replace("Kоэффициент", "Коэффициент")
    s = re.sub(r"\bпо субъектам Российской Федерации\b.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(19|20)\d{2}\s*г\.?\b.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(19|20)\d{2}\b.*$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\d+\)", "", s).strip()
    s = clean_text(s)

    m = re.search(r"(Коэффициент.+?на\s*1000\s*организаци[йя])", s, flags=re.IGNORECASE)
    if m:
        s = clean_text(m.group(1))

    if s.count("(") > s.count(")"):
        s += ")"
    return s


def find_indicator_title(df: pd.DataFrame) -> Optional[str]:
    max_rows = min(40, len(df))
    max_cols = min(20, df.shape[1])
    best = None
    best_len = 0
    for r in range(max_rows):
        for c in range(max_cols):
            s = clean_text(df.iat[r, c])
            if not s:
                continue
            low = s.lower()
            if "коэффициент" in low and "ликвидац" in low and "организац" in low:
                cand = normalize_indicator_title(s)
                if len(cand) > best_len:
                    best = cand
                    best_len = len(cand)
    return best


def parse_org_liquidation_ra_yearonly(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheets_from: int = 10,
    sheets_to: int = 18,
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    meta_sheets: Dict[str, Any] = {}

    for sh_i in range(sheets_from, sheets_to + 1):
        sh = str(sh_i)
        try:
            df = pd.read_excel(xlsx_path, sheet_name=sh, header=None, engine="openpyxl")

            header_row, year_col = find_year_col(df)
            if header_row is None or year_col is None:
                raise RuntimeError("Не найдена колонка 'За год'.")

            indicator_name = find_indicator_title(df)
            if not indicator_name:
                raise RuntimeError("Не найден заголовок показателя (коэффициент ликвидации организаций).")

            data_start = header_row + 1
            r_idx = find_row_by_firstcol(df, region_name, data_start)
            if r_idx is None:
                raise RuntimeError(f"Не найдена строка региона: {region_name}")

            value = to_number(df.iat[r_idx, year_col])
            if value is None:
                raise RuntimeError("В колонке 'За год' пусто/не число.")

            year = 2007 + sh_i

            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": indicator_name,
                    "value": value,
                    "unit_code": "на_1000_орг",
                }
            )

            meta_sheets[sh] = {"rows_count": 1, "year": year}

        except Exception as e:
            meta_sheets[sh] = {"rows_count": 0, "error": str(e)}

    return {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}) if rows else [],
            "sheets": meta_sheets,
        },
        "indicator_values": {"rows": rows},
    }


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/demo-org1_12-2025.xlsx"
    out_path = "/home/daria/altay-db/org_liquidation_ra_2017_2025.json"

    result = parse_org_liquidation_ra_yearonly(xlsx_path)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
