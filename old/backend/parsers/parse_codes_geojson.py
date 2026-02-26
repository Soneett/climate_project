import pandas as pd
import json
import re
from pathlib import Path
from unidecode import unidecode

def normalize_name(name):
    if not isinstance(name, str):
        return ""
    name = unidecode(name.strip().lower())

    name = re.sub(r'[\"\'\(\)\-]', '', name)
    return name

BASE_DIR = Path(__file__).resolve().parents[1]
geojson_file = BASE_DIR / "data" / "altai.geojson"

excel_file = BASE_DIR / "data" /"oktmo.xlsx"  
df = pd.read_excel(excel_file, header=None)

settlements = {} 
districts = {}     

parent_oktmo = None
parent_name = None

for index, row in df.iterrows():
    col_a = str(row[0]).strip() if not pd.isna(row[0]) else ""
    col_b = str(row[1]).strip() if not pd.isna(row[1]) else ""
    col_c = str(row[2]).strip() if len(row) > 2 and not pd.isna(row[2]) else ""

    if re.match(r'^\d{8}$', col_b):
        parent_oktmo = col_b
        parent_name = normalize_name(col_c if col_c else col_a)
        districts[parent_name] = parent_oktmo
        continue

    if re.match(r'^\d{8}$', col_b) and col_c:
        settlement_name = normalize_name(col_a)
        settlements[settlement_name] = {
            "oktmo": col_b,
            "parent_oktmo": parent_oktmo
        }


with open(geojson_file, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    name = feature["properties"].get("name", "")
    name_norm = normalize_name(name)

    if name_norm in settlements:
        feature["properties"]["oktmo"] = settlements[name_norm]["oktmo"]
        feature["properties"]["parent_oktmo"] = settlements[name_norm]["parent_oktmo"]

    elif name_norm in districts:
        feature["properties"]["oktmo"] = districts[name_norm]
        feature["properties"]["parent_oktmo"] = None  
    else:
        feature["properties"]["oktmo"] = None
        feature["properties"]["parent_oktmo"] = None

output_file = "altai_oktmo.geojson"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(geojson_data, f, ensure_ascii=False, indent=2)

print(f"Готово! Сохранено в {output_file}")

