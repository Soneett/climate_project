#!/usr/bin/env python3

import json
import re
from pathlib import Path

#import pandas as pd


def _fix_hyphen_parts(parts):
    parts = [str(p).strip() for p in parts if str(p).strip() and not str(p).lower().startswith("unnamed")]
    if not parts:
        return ""
    fixed, i = [], 0
    while i < len(parts):
        cur = parts[i]
        if cur.endswith("-") and i + 1 < len(parts):
            cur = cur[:-1] + parts[i + 1]
            i += 1
        fixed.append(cur)
        i += 1
    return " ".join(fixed).strip()


def _norm_cols_remove_nan(cols):
    out = []
    for c in cols:
        s = str(c).replace("\xa0", " ").strip()
        s = re.sub(r"\s+", " ", s).lower()
        s = re.sub(r"[^\wа-яё0-9 _-]", "", s, flags=re.UNICODE)
        s = s.replace("-", " ")
        tokens = [t for t in re.split(r"[_\s]+", s) if t and t != "nan"]
        s = "_".join(tokens)
        s = re.sub(r"^(?:nan_)+", "", s)
        s = re.sub(r"_+", "_", s).strip("_")
        out.append(s or "col")
    return out


def _to_num(x):
    try:
        if pd.isna(x):
            return None
        v = float(str(x).replace(" ", "").replace(",", "."))
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def _detect_census_year(df0):
    for r in range(0, 15):
        for v in df0.iloc[r].tolist():
            m = re.search(r"(20\d{2})", str(v))
            if m:
                return int(m.group(1))
    return None


def _fix_mojibake(s: str) -> str:
    s = str(s).strip()
    if not s:
        return s
    if "Р" in s or "С" in s:
        try:
            fixed = s.encode("cp1251", errors="ignore").decode("utf-8", errors="ignore").strip()
            if fixed:
                return fixed
        except Exception:
            pass
    return s


def _normalize_age_code(x) -> str:
    s = str(x).replace("\xa0", " ").strip()
    s = _fix_mojibake(s)
    s = re.sub(r"\s+", " ", s).strip()

    low = s.lower()

    if re.fullmatch(r"\d+", s):
        return s

    if re.fullmatch(r"\d+\s*-\s*\d+", s):
        return re.sub(r"\s*-\s*", "-", s)

    if low in {
        "100 и старше",
        "100и старше",
        "100_и_старше",
        "100 и старшe",
    }:
        return "100 и старше"

    if "100" in low and "стар" in low:
        return "100 и старше"

    if low in {
        "все возрасты",
        "все возраста",
        "все",
        "итого",
        "всего",
        "all",
    }:
        return "ALL"

    return s


def _is_age_row(age_code: str) -> bool:
    if age_code == "ALL":
        return True
    if re.fullmatch(r"\d+", age_code):
        return True
    if re.fullmatch(r"\d+-\d+", age_code):
        return True
    if age_code == "100 и старше":
        return True
    return False


def parse_population_age_sex_file(xlsx_path: str) -> dict:
    df0 = pd.read_excel(xlsx_path, engine="openpyxl", header=None)
    df0 = df0.iloc[:, :11]

    h1 = df0.iloc[3].astype(str).fillna("")
    h2 = df0.iloc[4].astype(str).fillna("")
    h3 = df0.iloc[5].astype(str).fillna("")
    headers = [_fix_hyphen_parts([a, b, c]) for a, b, c in zip(h1, h2, h3)]

    df = df0.iloc[6:].reset_index(drop=True)
    df.columns = _norm_cols_remove_nan(headers)
    df = df.dropna(how="all").reset_index(drop=True)

    census_year = _detect_census_year(df0)

    age_col = 0
    all_col = 2
    male_col = 3
    female_col = 4

    pas_rows = []

    for _, r in df.iterrows():
        age_code = _normalize_age_code(r.iloc[age_col])

        if not _is_age_row(age_code):
            continue

        v = _to_num(r.iloc[all_col])
        if v is not None:
            pas_rows.append({
                "year": census_year,
                "age_code": age_code,
                "sex_code": "A",
                "value": v
            })

        v = _to_num(r.iloc[male_col])
        if v is not None:
            pas_rows.append({
                "year": census_year,
                "age_code": age_code,
                "sex_code": "M",
                "value": v
            })

        v = _to_num(r.iloc[female_col])
        if v is not None:
            pas_rows.append({
                "year": census_year,
                "age_code": age_code,
                "sex_code": "F",
                "value": v
            })

    has_all = any(r["age_code"] == "ALL" for r in pas_rows)

    if not has_all:
        total_a = sum(r["value"] for r in pas_rows if r["sex_code"] == "A" and r["age_code"] != "ALL")
        total_m = sum(r["value"] for r in pas_rows if r["sex_code"] == "M" and r["age_code"] != "ALL")
        total_f = sum(r["value"] for r in pas_rows if r["sex_code"] == "F" and r["age_code"] != "ALL")

        pas_rows.append({
            "year": census_year,
            "age_code": "ALL",
            "sex_code": "A",
            "value": total_a
        })
        pas_rows.append({
            "year": census_year,
            "age_code": "ALL",
            "sex_code": "M",
            "value": total_m
        })
        pas_rows.append({
            "year": census_year,
            "age_code": "ALL",
            "sex_code": "F",
            "value": total_f
        })

    return {
        "population_age_sex": {
            "rows": pas_rows
        }
    }


def save_json(data: dict, out_path: str) -> None:
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"saved: {out_file}")


if __name__ == "__main__":
    xlsx_path = "/home/daria/altay-db/Копия_Возрастно_половой_состав_населения_Республики_Алтай_на_1_января (4).xlsx"
    out_path = "/home/daria/altay-db/population_age_sex_result.json"

    data = parse_population_age_sex_file(xlsx_path)
    save_json(data, out_path)

    print("population_age_sex_rows:", len(data["population_age_sex"]["rows"]))
    print(json.dumps(data["population_age_sex"]["rows"][-12:], ensure_ascii=False, indent=2))
