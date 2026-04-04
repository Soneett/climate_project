#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from typing import Any, Dict, List, Optional, Tuple, Union

#import pandas as pd


# утилиты

def clean_text(x: Any) -> str:
    s = "" if x is None else str(x)
    s = s.replace("\xa0", " ").strip()
    s = re.sub(r"\s+", " ", s)
    return s

def to_number(x: Any) -> Optional[float]:
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = clean_text(x)
    if s == "":
        return None
    # убрать сноски и прочее(оставить цифры/знаки/разделители)
    s = re.sub(r"[^\d,.\-]", "", s)
    s = s.replace(",", ".")
    if s in ("", ".", "-"):
        return None
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except Exception:
        return None

def detect_year(x: Any) -> Optional[int]:
    s = clean_text(x)
    m = re.search(r"(19|20)\d{2}", s)
    return int(m.group(0)) if m else None

def infer_unit(top_part: str, sub_part: str) -> Optional[str]:
    t = (top_part + " " + sub_part).lower()
    if "тыс" in t and "руб" in t:
        return "тыс.руб"
    if "руб./месяц" in t or "руб/месяц" in t or ("руб" in t and "месяц" in t):
        return "руб/мес"
    if "%" in t or "в % к" in t:
        return "%"
    return None


# основной парсер

def parse_income_balance_xlsx(
    xlsx_path: str,
    *,
    region_name: str = "Республика Алтай",
    sheet: Union[int, str] = 0,
    header_row_top: int = 4,
    header_row_sub: int = 5,
    data_start_row: int = 6
) -> Dict[str, Any]:

    df0 = pd.read_excel(xlsx_path, sheet_name=sheet, header=None, engine="openpyxl")

    # 1) собрать 2-строчную шапку
    top_raw = [clean_text(v) for v in df0.iloc[header_row_top].tolist()]
    sub_raw = [clean_text(v) for v in df0.iloc[header_row_sub].tolist()]

    # 2) forward-fill верхней строки (чтобы "nan" не пролезал и пустоты подтягивались)
    top_ff: List[str] = []
    last = ""
    for v in top_raw:
        vv = clean_text(v)
        if vv and vv.lower() != "nan":
            last = vv
        top_ff.append(last)

    # 3) описания индикаторов по столбцам (кроме 0-го столбца с годом)
    col_specs: List[Tuple[int, str, Optional[str]]] = []
    for c in range(1, df0.shape[1]):
        t = clean_text(top_ff[c])     # верхняя часть
        s = clean_text(sub_raw[c])    # нижняя часть

        # чистим "nan"
        if t.lower() == "nan":
            t = ""
        if s.lower() == "nan":
            s = ""

        if not t and not s:
            continue

        # собираем имя показателя: без "nan - ..."
        if t and s:
            ind_name = f"{t} — {s}"
        else:
            ind_name = t or s

        ind_name = clean_text(ind_name)
        if not ind_name:
            continue

        unit = infer_unit(t, s)
        col_specs.append((c, ind_name, unit))

    # 4) данные по годам
    rows: List[Dict[str, Any]] = []
    for r in range(data_start_row, len(df0)):
        y = detect_year(df0.iloc[r, 0])
        if y is None:
            continue

        for (c, ind_name, unit) in col_specs:
            val = to_number(df0.iloc[r, c])
            if val is None:
                continue
            rows.append({
                "region_name": region_name,
                "year": y,
                "indicator_name": ind_name,
                "value": val,
                "unit_code": unit,   # может быть None, если не распознали
            })

    out = {
        "meta": {
            "file": str(xlsx_path),
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": sorted({r["year"] for r in rows}),
            "indicators_found": [s[1] for s in col_specs],
        },
        "indicator_values": {
            "rows": rows
        }
    }
    return out


# CLI

if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Копия Состав и структура денежных доходов и расходов населения Республики Алтай(2).xlsx"
    out_path = "/home/daria/altay-db/income_balance_altai.json"

    result = parse_income_balance_xlsx(
        xlsx_path,
        region_name="Республика Алтай",
        sheet=0,
        header_row_top=4,
        header_row_sub=5,
        data_start_row=6
    )

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
