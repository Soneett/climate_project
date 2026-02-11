import json
from pathlib import Path
from sqlalchemy.orm import Session

from parsers.regions import parse_regions

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "regions.json"

def load_regions(session: Session):
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    parse_regions(data, session)
