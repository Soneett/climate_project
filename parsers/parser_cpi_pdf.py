import json
import re
from typing import Any, Dict, List

import pdfplumber


def clean_num(s: str):
    s = s.strip().replace(" ", "")
    s = s.replace(",", ".")
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def parse_cpi_pdf(pdf_path: str, region_name: str = "Республика Алтай") -> Dict[str, Any]:
    text_parts: List[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if t:
                text_parts.append(t)

    text = "\n".join(text_parts)

    rows: List[Dict[str, Any]] = []
    pattern = re.compile(
        r"^(20\d{2}|19\d{2})\s+(\d+[.,]\d+)\s+(\d+[.,]\d+)\s+(\d+[.,]\d+)\s+(\d+[.,]\d+)\s*$"
    )

    for line in text.splitlines():
        line = line.strip()
        m = pattern.match(line)
        if not m:
            continue

        year = int(m.group(1))
        v_all = clean_num(m.group(2))
        v_food = clean_num(m.group(3))
        v_nonfood = clean_num(m.group(4))
        v_services = clean_num(m.group(5))

        mapping = [
            ("Индексы потребительских цен — все товары и услуги", v_all),
            ("Индексы потребительских цен — продовольственные товары", v_food),
            ("Индексы потребительских цен — непродовольственные товары", v_nonfood),
            ("Индексы потребительских цен — услуги", v_services),
        ]

        for indicator_name, value in mapping:
            if value is None:
                continue
            rows.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": indicator_name,
                    "value": value,
                    "unit_code": "%",
                }
            )

    years_found = sorted({r["year"] for r in rows})
    indicators_found = sorted({r["indicator_name"] for r in rows})

    return {
        "meta": {
            "file": pdf_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": years_found,
            "indicators_found": indicators_found,
        },
        "indicator_values": {"rows": rows},
    }


if __name__ == "__main__":
    pdf_path = "/home/daria/altay-db/Индексы потребительских цен на  товары и услуги по Республике Алтай(3).pdf"
    out_path = "/home/daria/altay-db/cpi_altai.json"

    result = parse_cpi_pdf(pdf_path, region_name="Республика Алтай")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"][:5], "...", result["meta"]["years_found"][-5:])
    print("First 5 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:5], ensure_ascii=False, indent=2))
