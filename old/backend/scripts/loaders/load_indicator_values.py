import json
from pathlib import Path

from database import SessionLocal
from parsers.indicator_values import parse_indicator_values

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "birth_abs.json"

REGION_ID = 1
SOURCE_ID = 1


def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    rows = data.get("indicator_values", {}).get("rows", [])

    db = SessionLocal()
    try:
        parse_indicator_values(
            rows,
            db,
            region_id=REGION_ID,
            source_id=SOURCE_ID,
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
