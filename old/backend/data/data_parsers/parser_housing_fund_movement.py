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

    if isinstance(x, float):
        if math.isnan(x):
            return None
        return int(x) if x.is_integer() else float(x)

    s = clean_text(x)

    if s in ("", "-", "—", "–"):
        return None

    s = s.replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)

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
    if not m:
        return None
    return int(m.group(0))


def shorten_indicator_name(name: str) -> str:
    s = clean_text(name)

    s = re.sub(r",?\s*тыс\.?\s*м2\.?$", "", s, flags=re.IGNORECASE)
    s = re.sub(r",?\s*тыс\.?\s*м²\.?$", "", s, flags=re.IGNORECASE)
    s = re.sub(r",?\s*тыс\.?\s*кв\.?\s*м\.?$", "", s, flags=re.IGNORECASE)

    s = s.replace(" - ", " — ")

    s = re.sub(r"\s+", " ", s).strip(" ,")

    return s


def read_excel_auto(path: str):
    if path.lower().endswith(".xlsx"):
        return pd.read_excel(path, header=None, engine="openpyxl")
    return pd.read_excel(path, header=None, engine="xlrd")


def parse_housing_fund_movement_xls(
    xlsx_path: str,
    region_name: str = "Республика Алтай",
):
    df0 = read_excel_auto(xlsx_path)

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
    current_group: Optional[str] = None

    for r in range(year_row_idx + 1, len(df0)):
        raw_name = clean_text(
            df0.iat[r, 1] if df0.shape[1] > 1 else df0.iat[r, 0]
        )

        if raw_name == "":
            continue

        low = raw_name.lower()

        if low == "в том числе:":
            continue

        if raw_name in ("А", "Б", "В"):
            continue

        numeric_present = False

        for c in year_cols.keys():
            if c < df0.shape[1] and to_number(df0.iat[r, c]) is not None:
                numeric_present = True
                break

        if not numeric_present:
            continue

        is_main = (
            " - всего" in low
            or "– всего" in low
            or "— всего" in low
        )

        if is_main:
            current_group = shorten_indicator_name(raw_name)
            indicator_name = current_group
        else:
            short_name = shorten_indicator_name(raw_name)

            if short_name in ("А", "Б", "В"):
                continue

            if current_group:
                indicator_name = f"{current_group} — {short_name}"
            else:
                indicator_name = short_name

        indicator_name = re.sub(r"\s+", " ", indicator_name).strip()

        if indicator_name in ("А", "Б", "В"):
            continue

        for c, year in year_cols.items():
            if c >= df0.shape[1]:
                continue

            val = to_number(df0.iat[r, c])

            if val is None:
                continue

            val = val * 1000
            if isinstance(val, float) and val.is_integer():
                val = int(val)

            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": indicator_name,
                    "value": val,
                    "unit_code": "м2",
                }
            )

    return {
        "meta": {
            "file": xlsx_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
        },
        "indicator_values": {"rows": rows},
    }


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Копия загрузка Движение жилищногго фонда.xls"
    out_path = "/home/daria/altay-db/housing_fund_movement_altai.json"

    result = parse_housing_fund_movement_xls(
        xlsx_path=xlsx_path,
        region_name="Республика Алтай",
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("OK:", result["meta"]["rows_count"])
    print("Years:", result["meta"]["years_found"])
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
