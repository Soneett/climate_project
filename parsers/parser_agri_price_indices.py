import json
import re
from typing import Any, Dict, List, Optional

import pdfplumber


def clean_spaces(s: str) -> str:
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def to_float_ru(s: str) -> Optional[float]:
    s = clean_spaces(s)
    if not s:
        return None
    s = s.replace(",", ".")
    s = re.sub(r"[^\d.\-]", "", s)
    if s in ("", ".", "-"):
        return None
    try:
        return float(s)
    except Exception:
        return None


def parse_producer_price_index_agri_pdf(
    pdf_path: str,
    region_name: str = "Республика Алтай",
) -> Dict[str, Any]:
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join((p.extract_text() or "") for p in pdf.pages)

    text = clean_spaces(text.replace("\n", " "))
    years = re.findall(r"\b(19\d{2}|20\d{2})\b", text)
    years_int = [int(y) for y in years]

    rows: List[Dict[str, Any]] = []

    pattern = re.compile(
        r"\b(19\d{2}|20\d{2})\b\s+([0-9]+(?:[.,][0-9]+)?)\s+([0-9]+(?:[.,][0-9]+)?)\s+([0-9]+(?:[.,][0-9]+)?)\b"
    )

    for m in pattern.finditer(text):
        year = int(m.group(1))
        v1 = to_float_ru(m.group(2))
        v2 = to_float_ru(m.group(3))
        v3 = to_float_ru(m.group(4))

        if v1 is None or v2 is None or v3 is None:
            continue

        rows.append(
            {
                "region_name": region_name,
                "year": year,
                "indicator_name": "Индексы цен производителей сельскохозяйственной продукции — Продукция сельского хозяйства",
                "value": v1,
                "unit_code": "%",
            }
        )
        rows.append(
            {
                "region_name": region_name,
                "year": year,
                "indicator_name": "Индексы цен производителей сельскохозяйственной продукции — Продукция растениеводства",
                "value": v2,
                "unit_code": "%",
            }
        )
        rows.append(
            {
                "region_name": region_name,
                "year": year,
                "indicator_name": "Индексы цен производителей сельскохозяйственной продукции — Продукция животноводства",
                "value": v3,
                "unit_code": "%",
            }
        )

    years_found = sorted({r["year"] for r in rows})

    return {
        "meta": {
            "file": pdf_path,
            "region_name": region_name,
            "rows_count": len(rows),
            "years_found": years_found,
        },
        "indicator_values": {"rows": rows},
    }


if __name__ == "__main__":
    pdf_path = "/home/daria/altay-db/Индексы цен производителей сельскохозяйственной продукции по Республике Алтай_(2).pdf"
    out_path = "/home/daria/altay-db/producer_prices_agri_altai.json"

    result = parse_producer_price_index_agri_pdf(pdf_path, region_name="Республика Алтай")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Years:", result["meta"]["years_found"])
    print("First 6 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:6], ensure_ascii=False, indent=2))
