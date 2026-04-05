#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from typing import Any, Dict, List, Optional

def _clean(s: str) -> str:
    """Очищает строку от лишних пробелов и неразрывных пробелов"""
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def _num(s: str):
    """Преобразует строку в число (float или int), удаляя лишние символы"""
    if not s:
        return None
    s = _clean(s)
    s = s.replace(" ", "")
    s = s.replace(",", ".")
    s = re.sub(r"[^\d.-]", "", s)
    if s in ("", ".", "-"):
        return None
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except (ValueError, TypeError):
        return None

def _search(pattern: str, text: str, flags=0) -> Optional[re.Match]:
    """Вспомогательная функция для поиска по регулярному выражению."""
    return re.search(pattern, text, flags)

def parse_roads_pdf(pdf_path: str, region_name: str = "Республика Алтай") -> Dict[str, Any]:
    """
    Парсит PDF-файл и извлекает ключевые показатели
    """
    import pdfplumber

    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for p in pdf.pages:
                t = p.extract_text() or ""
                pages.append(t)
    except Exception as e:
        print(f"Ошибка при чтении PDF-файла: {e}")
        return {}

    text = _clean("\n".join(pages))
    
    year = None
    m = _search(r"по состоянию на конец\s*(\d{4})\s*года", text, flags=re.IGNORECASE)
    if m:
        year = int(m.group(1))
    
    rows: List[Dict[str, Any]] = []

    def emit(indicator_name: str, value, unit_code: str):
        if value is None:
            return
        rows.append(
            {
                "region_name": region_name,
                "year": year,
                "indicator_name": indicator_name,
                "value": value,
                "unit_code": unit_code,
            }
        )


    # 1. Общая протяженность
    m = _search(r"общая протяженность .*? составила\s*([0-9.,]+)\s*тыс\.\s*километр", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Автомобильные дороги — общая протяженность", _num(m.group(1)) * 1000, "км")

    # 2. С твердым покрытием
    m = _search(r"с твердым покрытием\s*[–-]\s*([0-9.,]+)\s*тыс\.\s*километров?\s*\(\s*([0-9.,]+)\s*%\)", text, re.IGNORECASE)
    if m:
        if m.group(1):
            emit("Автомобильные дороги — с твердым покрытием", _num(m.group(1)) * 1000, "км")
        if m.group(2):
            emit("Автомобильные дороги — доля с твердым покрытием", _num(m.group(2)), "%")
            
    # 3. С усовершенствованным покрытием
    m = _search(r"([0-9.,]+)\s*тыс\.\s*километров\s*\(\s*([0-9.,]+)\s*%\s*от общей протяженности\)\s*-\s*с усовершенствованным покрытием", text, re.IGNORECASE)
    if m:
        if m.group(1):
            emit("Автомобильные дороги — с усовершенствованным покрытием", _num(m.group(1)) * 1000, "км")
        if m.group(2):
            emit("Автомобильные дороги — доля с усовершенствованным покрытием", _num(m.group(2)), "%")

    # 4. Дороги общего пользования
    m = _search(r"([0-9.,]+)\s*тыс\.\s*километров дорог общего пользования", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Дороги общего пользования — протяженность", _num(m.group(1)) * 1000, "км")

    # 5. Дороги необщего пользования
    m = _search(r"([0-9.,]+)\s*тыс\.\s*километров дорог необщего пользования", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Дороги необщего пользования — протяженность", _num(m.group(1)) * 1000, "км")

    m = _search(r"\(соответственно\s*([0-9.,]+)\s*и\s*([0-9.,]+)\s*%\s*\)", text, re.IGNORECASE)
    if m:
        if m.group(1):
            emit("Доля дорог общего пользования", _num(m.group(1)), "%")
        if m.group(2):
            emit("Доля дорог необщего пользования", _num(m.group(2)), "%")
    
    m = _search(r"доля дорог, не отвечающих .*? требованиям, составляла .*?\s*([0-9.,]+)\s*%", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Дороги общего пользования (рег./межмун.) — доля не соответствующих нормативным требованиям", _num(m.group(1)), "%")

    # 6. Дороги местного значения)
    m = _search(r"местного значения с твердым покрытием составила\s*([0-9.,]+)\s*тыс\.\s*километров?\s*\(\s*([0-9.,]+)\s*%", text, re.IGNORECASE)
    if m:
        if m.group(1):
            emit("Дороги местного значения — с твердым покрытием", _num(m.group(1)) * 1000, "км")
        if m.group(2):
            emit("Дороги местного значения — доля с твердым покрытием", _num(m.group(2)), "%")
        
    m = _search(r"удельный вес дорог с твердым усовершенствованным покрытием\s*[–-]\s*([0-9.,]+)\s*%", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Дороги местного значения — доля с усовершенствованным покрытием", _num(m.group(1)), "%")

    m = _search(r"в этой категории дорог\s*-\s*([0-9.,]+)\s*%", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Дороги местного значения — доля не соответствующих нормативным требованиям", _num(m.group(1)), "%")
    
    # 7. Плотность дорог
    m = _search(r"Плотность .*?-\s*([0-9.,]+)\s*километров дорог на 1000 кв\.\s*км территории", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Плотность дорог с твердым покрытием", _num(m.group(1)), "км/1000км2")

    m = _search(r"\(\s*([0-9.,]+)\s*и\s*([0-9.,]+)\s*километров соответственно\s*\)", text, re.IGNORECASE)
    if m:
        if m.group(1):
            emit("Плотность дорог с твердым покрытием — среднероссийский уровень", _num(m.group(1)), "км/1000км2")
        if m.group(2):
            emit("Плотность дорог с твердым покрытием — среднесибирский уровень", _num(m.group(2)), "км/1000км2")
    
    m = _search(r"занимает\s*(\d+)\s*место среди регионов СФО", text, re.IGNORECASE)
    if m and m.group(1):
        emit("Место в СФО по плотности дорог с твердым покрытием", int(m.group(1)), "место")

    # 8. Данные из конца документа
    m = _search(r"(\d{4,}[,.]\d)\s*км\s*–\s*протяженность автомобильных дорог", text, re.IGNORECASE)
    if m:
        emit("Автомобильные дороги — общая протяженность (точная)", _num(m.group(1)), "км")

    m = _search(r"Протяженность автомобильных дорог общего пользования всего\s*–\s*([0-9.,]+)\s*км", text, re.IGNORECASE)
    if m:
        emit("Дороги общего пользования — протяженность (точная)", _num(m.group(1)), "км")

    m = _search(r"в том числе с твердым покрытием\s*([0-9.,]+)\s*км", text, re.IGNORECASE)
    if m:
        emit("Дороги общ. польз. с твердым покрытием (точная)", _num(m.group(1)), "км")

    m = _search(r"из них с усовершенствованным покрытием\s*-\s*([0-9.,]+)\s*км", text, re.IGNORECASE)
    if m:
        emit("Дороги общ. польз. с усоверш. покрытием (точная)", _num(m.group(1)), "км")

    out: Dict[str, Any] = {
        "meta": {
            "file": pdf_path,
            "region_name": region_name,
            "year_detected": year,
            "rows_count": len(rows),
        },
        "indicator_values": {"rows": rows},
    }
    return out

if __name__ == "__main__":
    pdf_path = "Пресс-выпуск дороги РА.pdf"
    out_path = "roads_altai_2019.json"
    
    result = parse_roads_pdf(pdf_path, region_name="Республика Алтай")
    
    if result and result.get("indicator_values", {}).get("rows"):
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"OK: сохранено {result['meta']['rows_count']} строк в файл {out_path}")
        print("Обнаруженный год:", result["meta"]["year_detected"])
        
        print("\n--- Пример извлеченных данных (полный список) ---")
        print(json.dumps(result["indicator_values"], ensure_ascii=False, indent=2))
    else:
        print("Не удалось извлечь данные из файла.")
