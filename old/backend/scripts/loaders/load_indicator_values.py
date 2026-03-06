import json
from pathlib import Path
from sqlalchemy.orm import Session

from parsers.indicator_values import parse_indicator_values

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "indicator_values"


def load_indicator_values(session: Session):
    for json_file in DATA_DIR.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            payload = json.load(f)

        parse_indicator_values(payload, session, source_file=json_file.name)
