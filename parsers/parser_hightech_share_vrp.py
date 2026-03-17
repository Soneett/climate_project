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


def extract_year(x: Any) -> Optional[int]:
    s = clean_text(x)
    m = re.search(r"(19|20)\d{2}", s)
    if not m:
        return None
    try:
        return int(m.group(0))
    except Exception:
        return None


def normalize_indicator_name(title: str) -> str:
    t = clean_text(title)
    t = re.sub(r"\*.*$", "", t).strip()
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_hightech_share_vrp_xlsx(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
    sheet: int = 0,
) -> Dict[str, Any]:
    df = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    title = normalize_indicator_name(df.iloc[0, 0] if df.shape[0] > 0 else "")
    if not title:
        title = "Доля продукции высокотехнологичных и наукоемких отраслей в ВРП"

    header_row_idx = None
    year_cols: Dict[int, int] = {}

    for r in range(len(df)):
        years_here: Dict[int, int] = {}
        for c in range(df.shape[1]):
            y = extract_year(df.iloc[r, c])
            if y is not None:
                years_here[c] = y
        if len(years_here) >= 2:
            header_row_idx = r
            year_cols = years_here
            break

    if header_row_idx is None:
        raise RuntimeError("Не удалось найти строку с годами.")

    target_row_idx = None
    for r in range(header_row_idx + 1, len(df)):
        if clean_text(df.iloc[r, 0]) == region_name:
            target_row_idx = r
            break

    rows: List[Dict[str, Any]] = []
    if target_row_idx is not None:
        for c, year in year_cols.items():
            val = to_number(df.iloc[target_row_idx, c])
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
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
        },
        "indicator_values": {"rows": rows},
    }
    return out


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Доля продукции высокотехнологичных и наукоемких отраслей в ВРП (с 2016 г.)(9).xlsx"
    out_path = "/home/daria/altay-db/hightech_share_vrp_altai.json"

    result = parse_hightech_share_vrp_xlsx(xlsx_path, region_name="Республика Алтай", sheet=0)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
