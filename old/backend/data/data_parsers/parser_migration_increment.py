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


def leading_spaces(x: Any) -> int:
    if x is None:
        return 0
    if isinstance(x, float) and math.isnan(x):
        return 0
    s = str(x).replace("\xa0", " ")
    m = re.match(r"^\s*", s)
    return len(m.group(0)) if m else 0


def to_number(x: Any):
    if x is None:
        return None
    if isinstance(x, float) and math.isnan(x):
        return None
    s = clean_text(x)
    if s == "":
        return None
    s = s.replace("—", "-").replace("–", "-").replace("−", "-")
    if re.fullmatch(r"[-]+", s):
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


def find_year_row(df0: pd.DataFrame, max_scan_rows: int = 50) -> Tuple[int, Dict[int, int]]:
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


def find_section_row(df0: pd.DataFrame, title: str) -> int:
    t0 = clean_text(title).lower()
    for r in range(len(df0)):
        s = clean_text(df0.iloc[r, 0]).lower()
        if s == t0:
            return r
    raise RuntimeError(f"Не удалось найти раздел: {title}")


def is_stop_row(name: str) -> bool:
    n = clean_text(name)
    if n == "":
        return True
    if re.match(r"^\d+\)", n):
        return True
    if n.lower().startswith("по итогам"):
        return True
    return False


def is_skip_label(name: str) -> bool:
    n = clean_text(name).lower()
    if n in ("из нее:", "из нее", "в том числе:", "в том числе"):
        return True
    return False


def parse_migration_increment_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
    section_title: str = "Миграционный прирост",
    unit_code: str = "чел",
) -> Dict[str, Any]:
    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    year_row_idx, year_cols = find_year_row(df0)
    section_row_idx = find_section_row(df0, section_title)

    rows: List[Dict[str, Any]] = []

    current_group: Optional[str] = None
    section_prefix = section_title

    for r in range(section_row_idx + 1, len(df0)):
        raw0 = df0.iloc[r, 0]
        name_clean = clean_text(raw0)

        if is_stop_row(name_clean):
            break

        if is_skip_label(name_clean):
            continue

        any_num = any(to_number(df0.iloc[r, c]) is not None for c in year_cols.keys())
        if not any_num:
            continue

        indent = leading_spaces(raw0)
        is_sub = indent >= 2 and current_group is not None

        if is_sub:
            indicator_name = f"{section_prefix} — {current_group} — {name_clean}"
        else:
            current_group = name_clean
            indicator_name = f"{section_prefix} — {name_clean}"

        for c, year in sorted(year_cols.items(), key=lambda x: x[1]):
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue
            rows.append(
                {
                    "region_name": region_name,
                    "year": int(year),
                    "indicator_name": indicator_name,
                    "value": val,
                    "unit_code": unit_code,
                }
            )

    out: Dict[str, Any] = {
        "meta": {
            "file": xlsx_path,
            "section": section_title,
            "rows_count": len(rows),
            "years_found": sorted({x["year"] for x in rows}),
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Общие итоги миграции населения РА(2).xlsx"
    out_path = "/home/daria/altay-db/migration_increment_altai.json"

    result = parse_migration_increment_xlsx(
        xlsx_path=xlsx_path,
        region_name="Республика Алтай",
        sheet=0,
        section_title="Миграционный прирост",
        unit_code="чел",
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
