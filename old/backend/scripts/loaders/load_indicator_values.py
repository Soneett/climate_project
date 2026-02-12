import json
from pathlib import Path
from sqlalchemy.orm import Session

from tables.regions import RegionsTable
from tables.data_sources import DataSourcesTable
from parsers.indicator_values import parse_indicator_values

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "indicator_values"

def load_indicator_values(session: Session):

    regions_map = {
        r.name: r.id
        for r in session.query(RegionsTable).all()
    }

    sources_map = {
        s.name: s.id
        for s in session.query(DataSourcesTable).all()
    }

    for json_file in DATA_DIR.glob("*.json"):
        with open(json_file, encoding="utf-8") as f:
            payload = json.load(f)

        metadata = payload["metadata"]

        region_name = metadata["region_name"]
        source_name = metadata["source_name"]

        region_id = regions_map[region_name]
        source_id = sources_map[source_name]

        rows = (
            payload
            .get("indicator_values", {})
            .get("rows", [])
        )

        if not rows:
            continue

        parse_indicator_values(
            rows,
            session,
            region_id=region_id,
            source_id=source_id,
        )

