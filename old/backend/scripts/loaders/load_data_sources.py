import json
from pathlib import Path
from sqlalchemy.orm import Session

from parsers.data_sources import parse_data_sources

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "data_sources.json"

def load_data_sources(session: Session):
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    parse_data_sources(data, session)
