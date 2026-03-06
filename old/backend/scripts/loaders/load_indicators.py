import json
from pathlib import Path
from sqlalchemy.orm import Session

from parsers.indicators import parse_indicators

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "indicators.json"


def load_indicators(session: Session):
    if not JSON_PATH.exists():
        return

    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    parse_indicators(data, session)
