from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/api", tags=["Config"])

_FRONTEND_DB_PATH = Path(__file__).resolve().parents[2] / "frontend" / "web" / "db" / "db.json"


def _normalize_block_indicators(content_blocks: Any) -> Any:
    if not isinstance(content_blocks, dict):
        return content_blocks

    normalized = {}
    for section_id, blocks in content_blocks.items():
        if not isinstance(blocks, list):
            normalized[section_id] = blocks
            continue

        section_blocks = []
        for block in blocks:
            if not isinstance(block, dict):
                section_blocks.append(block)
                continue

            next_block = dict(block)
            indicators = next_block.get("indicators")
            if isinstance(indicators, str):
                next_block["indicators"] = [value.strip() for value in indicators.split(",") if value.strip()]

            section_blocks.append(next_block)

        normalized[section_id] = section_blocks

    return normalized


def _load_frontend_fallback() -> dict:
    try:
        payload = json.loads(_FRONTEND_DB_PATH.read_text(encoding="utf-8"))
    except Exception:
        payload = {}

    return {
        "contentBlocks": _normalize_block_indicators(payload.get("contentBlocks", {})),
        "subjectIndicators": payload.get("subjectIndicators", []),
        "objectIndicators": payload.get("objectIndicators", []),
        "relationsContentBlocks": payload.get("relationsContentBlocks", {}),
    }


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


def _get_config_or_fallback(session: Session, key: str, fallback):
    data = _load_json_config(session, key)
    if data in (None, {}, []):
        return fallback

    if key == "contentBlocks":
        return _normalize_block_indicators(data)

    return data


@router.get("/contentBlocks")
def get_content_blocks(session: Session = Depends(get_db)):
    fallback = _load_frontend_fallback()
    return _get_config_or_fallback(session, "contentBlocks", fallback["contentBlocks"])


@router.get("/subjectIndicators")
def get_subject_indicators(session: Session = Depends(get_db)):
    fallback = _load_frontend_fallback()
    return _get_config_or_fallback(session, "subjectIndicators", fallback["subjectIndicators"])


@router.get("/objectIndicators")
def get_object_indicators(session: Session = Depends(get_db)):
    fallback = _load_frontend_fallback()
    return _get_config_or_fallback(session, "objectIndicators", fallback["objectIndicators"])


@router.get("/relationsContentBlocks")
def get_relations_content(session: Session = Depends(get_db)):
    fallback = _load_frontend_fallback()
    return _get_config_or_fallback(session, "relationsContentBlocks", fallback["relationsContentBlocks"])
