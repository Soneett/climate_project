#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


def _clean(s):
    s = (str(s) if s is not None else "").replace("\xa0", " ").strip()
    return re.sub(r"\s+", " ", s)


def _to_num(x):
    try:
        if pd.isna(x):
            return None
        s = str(x).strip().replace("\u00a0", " ")
        s = s.replace("—", "").replace("–", "").replace("−", "")
        s = re.sub(r"[^\d,.\- ]+", "", s).replace(" ", "").replace(",", ".")
        if s in ("", "."):
            return None
        v = float(s)
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def process_births_deaths_natural_local(xlsx_path: str, sheet=0) -> Dict:
    df0 = pd.read_excel(xlsx_path, engine="openpyxl", sheet_name=sheet, header=None)

    rows: List[Dict] = []

    for i in range(3, len(df0)):
        year = _to_num(df0.iat[i, 0])
        if year is None:
            continue
        year = int(year)

        births = _to_num(df0.iat[i, 1])
        deaths = _to_num(df0.iat[i, 2])
        natural = _to_num(df0.iat[i, 3])
        infant_deaths = _to_num(df0.iat[i, 7])

        if births is not None:
            rows.append({
                "year": year,
                "value": births,
                "indicator_name": "births_abs"
            })

        if deaths is not None:
            rows.append({
                "year": year,
                "value": deaths,
                "indicator_name": "deaths_abs"
            })

        if infant_deaths is not None:
            rows.append({
                "year": year,
                "value": infant_deaths,
                "indicator_name": "infant_deaths_abs"
            })

        if natural is not None:
            rows.append({
                "year": year,
                "value": natural,
                "indicator_name": "natural_abs"
            })

    return {
        "indicator_values": {
            "rows_count": len(rows),
            "rows": rows
        }
    }


def save_json(data: dict, out_path: str) -> None:
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"saved: {out_file}")


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Копия Рождаемость, смертность и естественный прирост населения в Республике Алтай(2).xlsx"
    out_path = "/home/daria/altay-db/births_deaths_natural_result.json"

    out = process_births_deaths_natural_local(
        xlsx_path=xlsx_path,
        sheet=0
    )

    save_json(out, out_path)

    print("rows_count:", out["indicator_values"]["rows_count"])
    print(json.dumps(out["indicator_values"]["rows"][:12], ensure_ascii=False, indent=2))
