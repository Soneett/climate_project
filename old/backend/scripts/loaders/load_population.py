import json
from pathlib import Path

from database import SessionLocal
from parsers.population_age_sex import parse_population_rows

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "population"

REGION_ID = 1
SOURCE_ID = 1

def main():
    session = SessionLocal()
    try:
        for json_file in DATA_DIR.glob("*.json"):
            with open(json_file, encoding="utf-8") as f:
                payload = json.load(f)

            for block in payload.values():
                rows = block.get("rows", [])
                if not rows:
                    continue

                parse_population_rows(
                    rows,
                    session,
                    region_id=REGION_ID,
                    source_id=SOURCE_ID,
                )
    finally:
        session.close()


if __name__ == "__main__":
    main()
