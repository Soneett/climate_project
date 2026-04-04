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
    s = s.strip()
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
    s = s.replace("−", "-")
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


def find_year_total_column(df: pd.DataFrame) -> Optional[int]:
    scan_rows = min(len(df), 20)
    scan_cols = min(df.shape[1], 40)
    for r in range(scan_rows):
        for c in range(scan_cols):
            if "за год" in clean_text(df.iat[r, c]).lower():
                return c
    return None


def find_row_index_by_region(df: pd.DataFrame, region_name: str) -> Optional[int]:
    target = clean_text(region_name).lower()
    for r in range(len(df)):
        if clean_text(df.iat[r, 0]).lower() == target:
            return r
    return None


def extract_indicator_title(df: pd.DataFrame) -> str:
    scan_rows = min(len(df), 12)
    scan_cols = min(df.shape[1], 12)

    for r in range(scan_rows):
        row_texts = [clean_text(df.iat[r, c]) for c in range(scan_cols)]
        row_text = " ".join([t for t in row_texts if t])
        if not row_text:
            continue

        if "коэффициент" in row_text.lower() and "ликвидац" in row_text.lower():
            title = row_text
            title = re.sub(r"\s*\(?\s*оквэд.*$", "", title, flags=re.IGNORECASE)
            title = re.sub(r"\s*\(?\s*\d{4}\s*г\.?\s*\)?\s*\d*\)?\s*$", "", title, flags=re.IGNORECASE)
            title = re.sub(r"\d+\)\s*$", "", title).strip()
            title = title.replace("на 1000 организаций по субъектам Российской Федерации", "на 1000 организаций")
            title = title.replace("по субъектам Российской Федерации", "").strip(" ,;")
            if title:
                return title

    return "Коэффициент официальной ликвидации организаций на 1000 организаций"


def parse_demo_org2_altai_years(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheets_from: int = 10,
    sheets_to: int = 18,
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    sheet_meta: Dict[str, Any] = {}

    for sh in range(sheets_from, sheets_to + 1):
        sheet_name = str(sh)
        year = 2007 + sh  # 10->2017 ... 18->2025

        try:
            df = pd.read_excel(xlsx_path, sheet_name=sheet_name, header=None, engine="openpyxl")
        except Exception as e:
            sheet_meta[sheet_name] = {"ok": False, "error": str(e)}
            continue

        year_col = find_year_total_column(df)
        if year_col is None:
            sheet_meta[sheet_name] = {"ok": False, "error": "Не найдена колонка 'За год'."}
            continue

        r_idx = find_row_index_by_region(df, region_name)
        if r_idx is None:
            sheet_meta[sheet_name] = {"ok": False, "error": f"Не найдена строка региона '{region_name}'."}
            continue

        val = to_number(df.iat[r_idx, year_col])
        if val is None:
            sheet_meta[sheet_name] = {"ok": False, "error": "Значение 'За год' пустое/не число.", "row": r_idx, "col": year_col}
            continue

        indicator_name = extract_indicator_title(df)

        rows.append(
            {
                "region_name": region_name,
                "year": year,
                "indicator_name": indicator_name,
                "value": val,
                "unit_code": "на_1000_орг",
            }
        )

        sheet_meta[sheet_name] = {
            "ok": True,
            "year": year,
            "year_col": year_col,
            "row_idx": r_idx,
            "value": val,
        }

    out = {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
            "sheets": sheet_meta,
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/demo-org2_12-2025.xlsx"
    out_path = "/home/daria/altay-db/demo_org2_altai_2017_2025.json"

    result = parse_demo_org2_altai_years(
        xlsx_path=xlsx_path,
        region_name="Республика Алтай",
        sheets_from=10,
        sheets_to=18,
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
