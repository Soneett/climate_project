import json
import re
import math
from typing import Any, Dict, List, Optional

import pdfplumber


def clean_text(s: Any) -> str:
    if s is None:
        return ""
    if isinstance(s, float) and math.isnan(s):
        return ""
    t = str(s).replace("\xa0", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def parse_number_ru(x: str) -> Optional[float]:
    x = clean_text(x)
    if x == "":
        return None
    x = x.replace(",", ".")
    x = re.sub(r"[^\d.\-]", "", x)
    if x in ("", ".", "-", "-."):
        return None
    try:
        v = float(x)
        return int(v) if v.is_integer() else v
    except Exception:
        return None


def extract_year(full_text: str) -> Optional[int]:
    m = re.search(r"\bв\s+((?:19|20)\d{2})\s+году\b", full_text, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"\b((?:19|20)\d{2})\b", full_text)
    if m:
        return int(m.group(1))
    return None


def tokenize_row_tail(line: str) -> List[str]:
    line = clean_text(line)
    tokens = []
    i = 0
    while i < len(line):
        if line[i].isdigit():
            j = i + 1
            while j < len(line) and (line[j].isdigit() or line[j] in ",."):
                j += 1
            tokens.append(line[i:j])
            i = j
            continue
        if line[i] == "-":
            tokens.append("-")
            i += 1
            continue
        if line[i] == "…":
            j = i + 1
            while j < len(line) and line[j] != " ":
                j += 1
            tokens.append(line[i:j])
            i = j
            continue
        i += 1
    return tokens


def is_hidden_or_dash(tok: str) -> bool:
    tok = clean_text(tok)
    if tok == "-":
        return True
    if tok.startswith("…"):
        return True
    return False


def normalize_activity(activity: str) -> str:
    a = clean_text(activity)

    a = re.sub(r"(?i)\bв\s+том\s+числе\b.*$", "", a).strip()

    a = re.sub(r"(?i)по\s+видам\s+экономической\s+деятельности\s*:?", "", a).strip()

    a = re.sub(r"(?i)^\s*деятельности\s*:\s*", "", a).strip()

    a = re.sub(r"\s*\d+\)\s*$", "", a).strip()

    a = a.strip("—-:;,. ")
    return a


def parse_credit_debit_structure_pdf(
    pdf_path: str,
    region_name: str = "Республика Алтай",
) -> Dict[str, Any]:
    with pdfplumber.open(pdf_path) as pdf:
        pages_text = []
        for p in pdf.pages:
            t = p.extract_text() or ""
            pages_text.append(t)
        full_text = "\n".join(pages_text)

    year = extract_year(full_text)

    lines = [clean_text(x) for x in full_text.splitlines()]
    lines = [x for x in lines if x]

    start_idx = None
    for i, ln in enumerate(lines):
        if "в том числе по видам экономической" in ln.lower():
            start_idx = i + 1
            break
    if start_idx is None:
        start_idx = 0

    end_idx = len(lines)
    for i in range(start_idx, len(lines)):
        if re.match(r"^1\)", lines[i]):
            end_idx = i
            break

    body = lines[start_idx:end_idx]

    rows_out: List[Dict[str, Any]] = []

    def emit(activity: str, c_all, c_over, d_all, d_over):
        metrics = [
            ("Кредиторская задолженность — всего", c_all),
            ("Кредиторская задолженность — просроченная", c_over),
            ("Дебиторская задолженность — всего", d_all),
            ("Дебиторская задолженность — просроченная", d_over),
        ]
        for metric_name, tok in metrics:
            if tok is None:
                continue
            if is_hidden_or_dash(tok):
                continue
            val = parse_number_ru(tok)
            if val is None:
                continue
            indicator = f"{activity} — {metric_name}" if activity else metric_name
            rows_out.append(
                {
                    "region_name": region_name,
                    "year": year,
                    "indicator_name": indicator,
                    "value": val,
                    "unit_code": "%",
                }
            )

    current_name_parts: List[str] = []

    def flush_line(line: str):
        nonlocal current_name_parts
        tail_tokens = tokenize_row_tail(line)

        if not tail_tokens:
            current_name_parts.append(line)
            return

        if len(tail_tokens) > 4:
            tail_tokens = tail_tokens[-4:]

        name_part = line
        for tok in tail_tokens:
            name_part = name_part.replace(tok, " ")
        name_part = clean_text(name_part)

        if current_name_parts:
            activity_raw = clean_text(" ".join(current_name_parts + [name_part]))
        else:
            activity_raw = name_part

        activity = normalize_activity(activity_raw)
        if activity.lower() == "всего":
            activity = "Всего"

        c_all = tail_tokens[0] if len(tail_tokens) >= 1 else None
        c_over = tail_tokens[1] if len(tail_tokens) >= 2 else None
        d_all = tail_tokens[2] if len(tail_tokens) >= 3 else None
        d_over = tail_tokens[3] if len(tail_tokens) >= 4 else None

        emit(activity, c_all, c_over, d_all, d_over)
        current_name_parts = []

    for ln in body:
        lnl = ln.lower()

        if lnl.startswith("в том числе"):
            continue
        if "(на конец года" in lnl:
            continue
        if "задолженность" in lnl and ("кредиторская" in lnl or "дебиторская" in lnl):
            continue

        if any(tokenize_row_tail(ln)):
            flush_line(ln)
        else:
            current_name_parts.append(ln)

    out = {
        "meta": {
            "file": pdf_path,
            "region_name": region_name,
            "year_found": year,
            "rows_count": len(rows_out),
        },
        "indicator_values": {"rows": rows_out},
    }
    return out


if __name__ == "__main__":
    pdf_path = "/home/daria/altay-db/Структура кредит. и дебит. зад-ти(3).pdf"
    out_path = "/home/daria/altay-db/credit_debit_structure_altai.json"

    result = parse_credit_debit_structure_pdf(pdf_path, region_name="Республика Алтай")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"OK: saved {result['meta']['rows_count']} rows to {out_path}")
    print("Year:", result["meta"]["year_found"])
    print("First 10 rows sample:")
    print(json.dumps(result["indicator_values"]["rows"][:10], ensure_ascii=False, indent=2))
