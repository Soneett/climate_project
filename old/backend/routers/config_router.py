from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(tags=["Config"])


_EMPTY_BY_KEY = {
    "contentBlocks": {},
    "subjectIndicators": [],
    "objectIndicators": [],
    "relationsContentBlocks": {},
}


def _load_json_config(session: Session, key: str):
    """Read JSON config from DB; return empty structure when config/table is missing."""
    try:
        row = session.execute(
            text("SELECT value FROM frontend_config WHERE key = :key LIMIT 1"),
            {"key": key},
        ).fetchone()
    except Exception:
        return _EMPTY_BY_KEY[key]

    if not row:
        return _EMPTY_BY_KEY[key]

    raw_value = row[0]
    if raw_value is None:
        return _EMPTY_BY_KEY[key]

    if isinstance(raw_value, (dict, list)):
        return raw_value

    try:
        return json.loads(raw_value)
    except Exception:
        return _EMPTY_BY_KEY[key]


@router.get("/contentBlocks")
def get_content_blocks(session: Session = Depends(get_db)):
    return _load_json_config(session, "contentBlocks")


@router.get("/subjectIndicators")
def get_subject_indicators(session: Session = Depends(get_db)):
    return _load_json_config(session, "subjectIndicators")


@router.get("/objectIndicators")
def get_object_indicators(session: Session = Depends(get_db)):
    return _load_json_config(session, "objectIndicators")


@router.get("/relationsContentBlocks")
def get_relations_content(session: Session = Depends(get_db)):
    return _load_json_config(session, "relationsContentBlocks")
