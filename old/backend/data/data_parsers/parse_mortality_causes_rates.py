#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path
from typing import Optional, Dict, List

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


def _find_header_row(df0: pd.DataFrame) -> int:
    for i in range(min(30, len(df0))):
        row = [_clean(v) for v in df0.iloc[i].tolist()]
        years = sum(1 for v in row if re.fullmatch(r"(19|20)\d{2}", v or ""))
        if years >= 4:
            return i
    return 0


def _simplify_cause(text: str) -> str:
    s = _clean(text).lower()
    s = re.sub(r"^(в\s*том\s*числе|из\s*них)\s*:?\s*", "", s)
    s = re.sub(r"^\s*в\s*том\s*числе\s*", "", s)
    s = re.sub(r"^\s*из\s*них\s*", "", s)
    s = re.sub(r"^\s*от\s+", "", s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _slug_cause(s: str) -> str:
    t = _simplify_cause(s)
    if not t:
        return ""
    if "всех причин" in t or "умершие от всех причин" in t or t == "умершие":
        return "all_causes"
    if "кровообращ" in t:
        return "circulatory_diseases"
    if "новообраз" in t:
        return "neoplasms"
    if "внешних причин" in t or "внешние причины" in t:
        return "external_causes"
    if "транспортн" in t and "травм" in t:
        return "transport_injuries_all"
    if "дтп" in t:
        return "road_accidents"
    if "алкогол" in t and "отрав" in t:
        return "alcohol_poisoning"
    if "самоуби" in t:
        return "suicides"
    if "убийств" in t:
        return "homicides"
    if "органов дыхан" in t:
        return "respiratory_diseases"
    if "органов пищевар" in t:
        return "digestive_diseases"
    if "инфекцион" in t or "паразитар" in t:
        return "infectious_parasitic"
    if "туберкул" in t:
        return "tuberculosis"
    t = re.sub(r"[^\wа-яё0-9 ]+", "", t)
    t = re.sub(r"\s+", "_", t).strip("_")
    return t or "cause"


def process_mortality_causes_rates_local(
    xlsx_path: str,
    sheet: Optional[int] = 0
) -> Dict:
    df0 = pd.read_excel(xlsx_path, engine="openpyxl", sheet_name=sheet, header=None)

    hdr = _find_header_row(df0)
    head = [_clean(v) for v in df0.iloc[hdr].tolist()]

    cols = []
    for j, v in enumerate(head):
        if j == 0:
            cols.append("cause")
        else:
            m = re.fullmatch(r"(19|20)\d{2}", v or "")
            cols.append(int(m.group(0)) if m else f"col{j}")

    df = df0.iloc[hdr + 1:].copy()
    df.columns = cols
    df = df.loc[:, [c for c in df.columns if not (isinstance(c, str) and c.startswith("col"))]]
    df = df.dropna(how="all").reset_index(drop=True)

    rows: List[Dict] = []
    year_cols = [c for c in df.columns if isinstance(c, int)]

    if "cause" not in df.columns or not year_cols:
        return {"indicator_values": {"rows_count": 0, "rows": []}}

    for _, r in df.iterrows():
        cause_raw = _clean(r.get("cause", ""))
        if not cause_raw:
            continue

        test = cause_raw.lower()
        if re.fullmatch(r"(в\s*том\s*числе|из\s*них)\:?", test):
            continue
        if "показатели рассчитаны" in test or "перепис" in test or test.startswith("1)"):
            continue

        slug = _slug_cause(cause_raw)
        if not slug:
            continue

        key = f"death_rate_{slug}"

        for y in year_cols:
            val = _to_num(r.get(y))
            if val is None:
                continue
            rows.append({
                "year": int(y),
                "value": val,
                "indicator_name": key
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
    xlsx_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/sources/death_causes.xlsx"
    out_path = "C:/Users/kukoc/Desktop/2215/old/backend/data/indicator_values/death_causes.json"

    out = process_mortality_causes_rates_local(
        xlsx_path=xlsx_path,
        sheet=0
    )

    save_json(out, out_path)

    print("rows_count:", out["indicator_values"]["rows_count"])
    print(json.dumps(out["indicator_values"]["rows"][:10], ensure_ascii=False, indent=2))
