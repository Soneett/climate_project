import json
from pathlib import Path
from database import SessionLocal
from parsers.indicators import parse_indicators

BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "indicators.json"

def main():
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f).get("indicators", [])

    db = SessionLocal()
    try:
        parse_indicators(data, db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
