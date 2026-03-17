#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import re
from typing import Any, Dict, List, Optional

import pandas as pd


def clean_text(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and math.isnan(x):
        return ""
    s = str(x).replace("\xa0", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    s = s.replace("непродоволь- ственных", "непродовольственных")
    return s


def to_number(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    if isinstance(x, (int, float)):
        return int(x) if isinstance(x, float) and x.is_integer() else float(x)
    s = clean_text(x)
    if s == "":
        return None
    s = re.sub(r"[^0-9,.\-]", "", s)
    s = s.replace(",", ".")
    if s in ("", ".", "-"):
        return None
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def build_metric_names(df0: pd.DataFrame, header_rows: List[int]) -> Dict[int, str]:
    names: Dict[int, str] = {}
    ncols = df0.shape[1]
    for c in range(1, ncols):
        parts: List[str] = []
        for r in header_rows:
            if r >= len(df0):
                continue
            s = clean_text(df0.iloc[r, c])
            if not s:
                continue
            parts.append(s)
        name = " — ".join(parts)
        name = re.sub(r"^в том числе:\s*", "", name, flags=re.IGNORECASE)
        name = re.sub(r"^из них:\s*", "", name, flags=re.IGNORECASE)
        name = re.sub(r"\s+", " ", name).strip(" —")
        if name:
            names[c] = name
    return names


def parse_consumption_expenses_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:
    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    metric_names = build_metric_names(df0, header_rows=[3, 4, 5])

    rows: List[Dict[str, Any]] = []
    years_found = set()
    groups_found = set()

    current_group: Optional[str] = None

    for r in range(6, len(df0)):
        c0s = clean_text(df0.iloc[r, 0])

        is_year = bool(re.fullmatch(r"\d{4}", c0s))

        numeric_present = any(
            to_number(df0.iloc[r, c]) is not None for c in metric_names.keys()
        )

        other_nonempty = any(clean_text(df0.iloc[r, c]) for c in range(1, df0.shape[1]))

        if c0s and (not is_year) and (not numeric_present) and (not other_nonempty):
            current_group = c0s
            groups_found.add(current_group)
            continue

        if is_year:
            year = int(c0s)
            years_found.add(year)
            for c, metric in metric_names.items():
                val = to_number(df0.iloc[r, c])
                if val is None:
                    continue
                rows.append(
                    {
                        "region_name": region_name,
                        "year": year,
                        "indicator_name": f"{current_group} — {metric}" if current_group else metric,
                        "value": val,
                        "unit_code": "руб_мес",
                    }
                )

    out: Dict[str, Any] = {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted(years_found),
            "groups_found": sorted(groups_found),
        },
        "indicator_values": {
            "rows": rows
        },
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Состав расходов на потребление домашних хозяйств в Республике Алтай(2).xlsx"
    out_path = "/home/daria/altay-db/consumption_expenses_altai.json"

    result = parse_consumption_expenses_xlsx(xlsx_path, region_name="Республика Алтай", sheet=0)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("Groups:", result["meta"]["groups_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
