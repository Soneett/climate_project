import json
from pathlib import Path

from database import SessionLocal
from parsers.indicator_subtypes import parse_indicator_subtypes


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "indicator_subtypes.json"


def main():
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()
    try:
        parse_indicator_subtypes(data, db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
