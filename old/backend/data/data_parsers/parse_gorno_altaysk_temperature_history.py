import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup

MISSING_VALUES = {"999.9", "999.0", "99.9", "9999.0", "999"}

def _is_temp(x: str) -> Tuple[bool, Optional[float]]:
    """Проверяет, является ли строка значением температуры."""
    clean_x = x.strip().replace(",", ".")
    if clean_x in MISSING_VALUES:
        return True, None
    try:
        val = float(clean_x)
        return True, val
    except ValueError:
        return False, None

def _mean(values: List[Optional[float]]) -> Optional[float]:
    """Вычисляет среднее для списка, игнорируя None."""
    clean = [v for v in values if v is not None]
    if not clean:
        return None
    return round(sum(clean) / len(clean), 2)

def parse_pogodaiklimat_temperature_history(
    url: str,
    region_name: str,
) -> Dict[str, Any]:
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding

    soup = BeautifulSoup(response.text, "html.parser")
    # Получаем весь текст через пробел, чтобы игнорировать сложные HTML-таблицы
    text = soup.get_text(" ")
    tokens = text.split()

    # Ищем начало блока с температурами
    start_idx = -1
    for i, t in enumerate(tokens):
        if "Средние" in t and i + 2 < len(tokens) and "месячные" in tokens[i+1]:
            start_idx = i
            break
            
    # Ищем конец блока (переход к осадкам или координатам)
    end_idx = len(tokens)
    for i, t in enumerate(tokens):
        if "Расположение" in t and i + 1 < len(tokens) and "метеорологической" in tokens[i+1]:
            end_idx = i
            break
        elif "Месячные" in t and i + 2 < len(tokens) and "суммы" in tokens[i+2] and i > start_idx + 50:
            end_idx = i
            break
            
    if start_idx == -1:
        start_idx = 0
        
    block = tokens[start_idx:end_idx]
    
    # Ищем индекс слова "янв", чтобы разделить блок на годы и данные
    jan_idx = -1
    for i, t in enumerate(block):
        if t.lower() == "янв":
            jan_idx = i
            break
            
    if jan_idx != -1:
        # Ищем слово "год" перед "янв", чтобы точно определить начало списка годов
        god_idx = -1
        for i in range(jan_idx - 1, -1, -1):
            if block[i].lower() == "год":
                god_idx = i
                break
                
        if god_idx != -1:
            table_years_block = block[god_idx + 1 : jan_idx]
            data_block = block[jan_idx:]
        else:
            table_years_block = block[:jan_idx]
            data_block = block[jan_idx:]
    else:
        table_years_block = block
        data_block = block

    years: List[int] = []
    # Собираем годы из левого блока таблицы
    for t in table_years_block:
        if t.isdigit() and len(t) == 4 and 1800 <= int(t) <= 2100:
            years.append(int(t))
            
    # Если мы не нашли годы отдельно, значит это стандартная таблица (строка за строкой)
    extract_years_from_data = (len(years) == 0)
    
    temps: List[Optional[float]] = []
    # Собираем все температуры
    for t in data_block:
        if extract_years_from_data and t.isdigit() and len(t) == 4 and 1800 <= int(t) <= 2100:
            years.append(int(t))
            continue
            
        valid, val = _is_temp(t)
        if valid:
            temps.append(val)
            
    if not years:
        raise ValueError("Не удалось найти годы на странице.")
    if not temps:
        raise ValueError("Не удалось найти температуры на странице.")
        
    n_years = len(years)
    n_temps = len(temps)
    
    # Проверяем, есть ли колонка "откл." (отклонение от нормы), чтобы понять длину данных (13 или 14)
    header_tokens = []
    if jan_idx != -1:
        header_tokens = [t.lower() for t in block[jan_idx:jan_idx+20]]
        
    has_deviation = any("откл" in t for t in header_tokens)
    columns = 14 if has_deviation else 13
    
    rows: List[Dict[str, Any]] = []
    all_real_months: List[float] = [] # Хранилище всех валидных температур для расчета глобальных мин/макс
    
    # Защита от смещения: берем минимальное доступное количество строк
    n = min(n_years, n_temps // columns)
    
    for i in range(n):
        year = years[i]
        chunk = temps[i * columns : (i + 1) * columns]
        
        months = chunk[:12]
        annual = chunk[12] if len(chunk) > 12 else None
        
        real_months = [x for x in months if x is not None]
        if not real_months and annual is None:
            continue
            
        # Добавляем все месячные температуры текущего года в общий массив
        all_real_months.extend(real_months)
            
        rows.append({
            "region_name": region_name,
            "year": year,
            "avg_annual_temp": annual,
            "avg_summer_temp": _mean([months[5], months[6], months[7]]),
            "avg_winter_temp": _mean([months[0], months[1], months[11]]),
            "source_url": url,
        })

    if not rows:
        raise ValueError("Не удалось распарсить ни одной валидной строки с данными.")

    return {
        "source": url,
        "region_name": region_name,
        "rows": rows,
        "global_max": max(all_real_months) if all_real_months else None,
        "global_min": min(all_real_months) if all_real_months else None,
    }

def to_long_rows(parsed: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Исключили мин/макс из погодной разбивки
    mapping = {
        "avg_annual_temp": "Средняя годовая температура",
        "avg_summer_temp": "Средняя температура лета",
        "avg_winter_temp": "Средняя температура зимы",
    }
    
    result: List[Dict[str, Any]] = []
    
    # 1. Добавляем данные по годам
    for row in parsed["rows"]:
        for field, indicator_name in mapping.items():
            value = row.get(field)
            if value is None:
                continue
            result.append({
                "region_name": row["region_name"],
                "year": row["year"],
                "indicator_name": indicator_name,
                "value": round(value, 2),
                "unit_code": "degC",
                "source_url": row["source_url"],
            })
            
    # 2. Добавляем глобальные максимум и минимум (за всё время)
    region = parsed.get("region_name", "Unknown")
    source_url = parsed.get("source", "")
    
    if parsed.get("global_max") is not None:
        result.append({
            "region_name": region,
            "year": None, # Указываем None, так как это данные за весь период
            "indicator_name": "Максимальная зарегистрированная температура за всё время",
            "value": round(parsed["global_max"], 2),
            "unit_code": "degC",
            "source_url": source_url,
        })
        
    if parsed.get("global_min") is not None:
        result.append({
            "region_name": region,
            "year": None,
            "indicator_name": "Минимальная зарегистрированная температура за всё время",
            "value": round(parsed["global_min"], 2),
            "unit_code": "degC",
            "source_url": source_url,
        })
        
    return result

def save_json(rows: List[Dict[str, Any]], file_name: str) -> None:
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / file_name
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"saved: {out_path.resolve()}")

if __name__ == "__main__":
    data = parse_pogodaiklimat_temperature_history(
        url="https://www.pogodaiklimat.ru/history/36052.htm",
        region_name="Горно-Алтайск",
    )
    long_rows = to_long_rows(data)
    save_json(
        long_rows,
        "temperature_gorno_altaysk.json",
    )
    print(f"rows: {len(long_rows)}")
    print(long_rows[:5])
    print(f"\nАбсолютный максимум: {data.get('global_max')} degC")
    print(f"Абсолютный минимум: {data.get('global_min')} degC")
