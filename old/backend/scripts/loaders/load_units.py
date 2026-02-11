import json
from pathlib import Path
from sqlalchemy.orm import Session
from parsers.units import parse_units

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "units.json"

def load_units(session: Session):
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    parse_units(data, session)
    
