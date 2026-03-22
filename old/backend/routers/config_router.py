from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

router = APIRouter(prefix="/api", tags=["Config"])

def _load_json_config(session: Session, key: str):
    """Try to read JSON config from DB; return None when config/table is missing."""
    try:
        row = session.execute(
            text("SELECT value FROM frontend_config WHERE key = :key LIMIT 1"),
            {"key": key},
        ).fetchone()
    except Exception:
        return None

    if not row:
        return None

    raw_value = row[0]
    if raw_value is None:
        return None

    if isinstance(raw_value, (dict, list)):
        return raw_value

    try:
        return json.loads(raw_value)
    except Exception:
        return None

def _get_config_or_empty(session: Session, key: str, empty_value):
    data = _load_json_config(session, key)
    if data in (None, {}, []):
        return empty_value
    return data


@router.get("/contentBlocks")
def get_content_blocks(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "contentBlocks", {})


@router.get("/subjectIndicators")
def get_subject_indicators(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "subjectIndicators", [])


@router.get("/objectIndicators")
def get_object_indicators(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "objectIndicators", [])

@router.get("/relationsContentBlocks")
def get_relations_content(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "relationsContentBlocks", {})
