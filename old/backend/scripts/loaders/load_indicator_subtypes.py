import json
from pathlib import Path
from sqlalchemy.orm import Session
from parsers.indicator_subtypes import parse_indicator_subtypes

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "indicator_subtypes.json"


def load_indicator_subtypes(session: Session):
    if not JSON_PATH.exists():
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    parse_indicator_subtypes(data, session)
