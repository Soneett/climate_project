import json
import re
from typing import Dict, List, Optional

import pdfplumber


def clean_text(s: str) -> str:
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def extract_numbers(s: str) -> List[float]:
    s = s.replace("−", "-")
    tokens = re.findall(r"-?\d+(?:[.,]\d+)?", s)
    out: List[float] = []
    for t in tokens:
        t2 = t.replace(",", ".")
        try:
            out.append(float(t2))
        except Exception:
            continue
    return out


def detect_year_prefix(line: str) -> Optional[int]:
    m = re.match(r"^\s*(\d{4})", line)
    if not m:
        return None
    y = int(m.group(1))
    if 1900 <= y <= 2100:
        return y
    return None


def parse_employment_education_pdf(
    pdf_path: str,
    region_name: str = "Республика Алтай",
) -> Dict:
    with pdfplumber.open(pdf_path) as pdf:
        all_lines: List[str] = []
        for page in pdf.pages:
            txt = page.extract_text() or ""
            for ln in txt.splitlines():
                ln = clean_text(ln)
                if ln:
                    all_lines.append(ln)

    edu_cols = [
        "всего",
        "высшее",
        "среднее профессиональное (специалисты среднего звена)",
        "среднее профессиональное (квалифицированные рабочие/служащие)",
        "среднее общее",
        "основное общее",
        "без основного общего",
    ]

    sex_code = "A"
    mode = "abs"
    unit_code = "тыс_чел"

    rows: List[Dict] = []
    years_found = set()

    for ln in all_lines:
        low = ln.lower()

        if low in ("мужчины", "мужчины:"):
            sex_code = "M"
            continue
        if low in ("женщины", "женщины:"):
            sex_code = "F"
            continue
        if low in ("все", "всего", "итого"):
            sex_code = "A"

        if "в процентах к итогу" in low:
            mode = "pct"
            unit_code = "%"
            continue

        if low in ("занятые", "тыс. человек", "тыс.человек", "тыс. чел", "тыс.чел"):
            continue

        year = detect_year_prefix(ln)
        if year is None:
            continue

        rest = ln[len(str(year)) :].strip()
        nums = extract_numbers(rest)

        expected = len(edu_cols)
        if len(nums) > expected:
            nums = nums[:expected]
        if len(nums) < expected:
            continue

        years_found.add(year)

        base_name = "Занятые по уровню образования" if mode == "abs" else "Структура занятых по уровню образования"

        for i, col_name in enumerate(edu_cols):
            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": f"{base_name} — {col_name}",
                    "sex_code": sex_code,
                    "value": nums[i] if mode == "pct" else (int(nums[i]) if float(nums[i]).is_integer() else nums[i]),
                    "unit_code": unit_code,
                }
            )

    return {
        "meta": {
            "file": pdf_path,
            "region_name": region_name,
            "years_found": sorted(years_found),
            "rows_count": len(rows),
        },
        "indicator_values": {"rows": rows},
    }


if __name__ == "__main__":
    pdf_path = "/home/daria/altay-db/Численность и структура занятых в Республике Алтай по уровню образования(2).pdf"
    out_path = "/home/daria/altay-db/employment_education_altai.json"

    result = parse_employment_education_pdf(pdf_path, region_name="Республика Алтай")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
