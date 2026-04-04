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


def to_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None

    s = clean_text(x)
    if not s:
        return None

    s = re.sub(r"[^\d,.\-]", "", s).replace(",", ".")
    if s in ("", ".", "-"):
        return None

    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def detect_year_cell(x: Any) -> Optional[int]:
    s = clean_text(x)
    m = re.search(r"\b(19|20)\d{2}\b", s)
    return int(m.group(0)) if m else None


def strip_footnotes(s: str) -> str:
    return re.sub(r"\d+\)\s*$", "", s).strip()


def is_noise_row(name: str) -> bool:
    n = clean_text(name).lower()
    return n == "" or n.endswith(":") or n in ("из них", "из них:")


def find_header_rows(df0: pd.DataFrame) -> Tuple[int, int]:
    """
    Ищем две строки:
    1) строку с названиями блоков: «Всего заболеваний» и «На 1 000 человек населения»
    2) строку ниже — с годами (2018, 2019, …)
    """
    for r in range(min(40, len(df0))):
        row = [clean_text(v).lower() for v in df0.iloc[r].tolist()]
        row_join = " | ".join(row)

        if ("всего заболев" in row_join) and ("на 1 000" in row_join or "на 1000" in row_join):
            if r + 1 < len(df0):
                years = [detect_year_cell(v) for v in df0.iloc[r + 1].tolist()]
                if sum(1 for y in years if y is not None) >= 2:
                    return r, r + 1

    raise RuntimeError("Не удалось найти строки заголовков (блоки + годы).")


def build_year_map(df0: pd.DataFrame, group_row: int, year_row: int) -> Dict[str, Dict[int, int]]:
    group_cells = [clean_text(v) for v in df0.iloc[group_row].tolist()]
    year_cells = df0.iloc[year_row].tolist()

    total_cols: Dict[int, int] = {}
    per1000_cols: Dict[int, int] = {}

    current_block = None

    for c in range(len(group_cells)):
        g = clean_text(group_cells[c]).lower()

        if "всего заболев" in g:
            current_block = "total"
        elif ("на 1 000" in g) or ("на 1000" in g):
            current_block = "per1000"

        y = detect_year_cell(year_cells[c])
        if y is None:
            continue

        if current_block == "total":
            total_cols[y] = c
        elif current_block == "per1000":
            per1000_cols[y] = c

    if not total_cols or not per1000_cols:
        raise RuntimeError("Не удалось определить столбцы годов для обоих блоков.")

    return {"total": total_cols, "per1000": per1000_cols}


def parse_morbidity_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:

    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    group_row, year_row = find_header_rows(df0)
    colmap = build_year_map(df0, group_row, year_row)

    total_label = "Всего заболеваний"
    per1000_label = "На 1 000 человек населения"

    rows: List[Dict[str, Any]] = []

    for r in range(year_row + 1, len(df0)):
        disease = clean_text(df0.iloc[r, 0])
        if is_noise_row(disease):
            continue

        any_num = False
        for c in colmap["total"].values():
            if to_number(df0.iloc[r, c]) is not None:
                any_num = True
                break

        if not any_num:
            for c in colmap["per1000"].values():
                if to_number(df0.iloc[r, c]) is not None:
                    any_num = True
                    break

        if not any_num:
            continue

        for year, c in sorted(colmap["total"].items()):
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue
            rows.append({
                "region_name": region_name,
                "year": year,
                "indicator_name": f"{disease} — {total_label}",
                "value": val,
                "unit_code": "случаев",
            })

        for year, c in sorted(colmap["per1000"].items()):
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue
            rows.append({
                "region_name": region_name,
                "year": year,
                "indicator_name": f"{disease} — {strip_footnotes(per1000_label)}",
                "value": val,
                "unit_code": "на_1000_нас",
            })

    return {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
            "group_row": group_row,
            "year_row": year_row,
            "cols_total": colmap["total"],
            "cols_per1000": colmap["per1000"],
        },
        "indicator_values": {
            "rows": rows
        }
    }


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Заболеваемость населения по основным классам болезней в Республике Алтай(4).xlsx"
    out_path = "/home/daria/altay-db/morbidity_altai.json"

    result = parse_morbidity_xlsx(
        xlsx_path,
        region_name="Республика Алтай",
        sheet=0
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
