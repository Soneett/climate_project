from __future__ import annotations

import json

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db
from tables.indicator_values import IndicatorValuesTable
from tables.indicators import IndicatorsTable

router = APIRouter(prefix="/api", tags=["Config"])

_TYPE_TO_SECTION = {
    "демография": "s1",
    "уровень жизни": "s2",
    "здравоохранение": "s3",
    "образование": "s4",
    "экономика": "s5",
    "инфраструктура": "s6",
    "температура": "c1",
    "осадки": "c2",
    "ветер": "c3",
    "природные катаклизмы": "c4",
    "экология": "c5",
    "бюджет": "g1",
}


def _normalize_text(value: str | None) -> str:
    return (value or "").strip().lower()


def _resolve_section_id(indicator_type: str | None, theme: str | None) -> str:
    type_key = _normalize_text(indicator_type)
    theme_key = _normalize_text(theme)

    if type_key in _TYPE_TO_SECTION:
        return _TYPE_TO_SECTION[type_key]

    if "катаклизм" in theme_key or "чс" in theme_key:
        return "c4"
    if "температур" in theme_key:
        return "c1"
    if "осад" in theme_key:
        return "c2"
    if "ветер" in theme_key:
        return "c3"
    if "эколог" in theme_key:
        return "c5"

    return "s5"


def _chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def _build_content_blocks_from_db(session: Session) -> dict[str, list[dict]]:
    rows = (
        session.query(IndicatorsTable)
        .join(IndicatorValuesTable, IndicatorValuesTable.indicator_id == IndicatorsTable.id)
        .filter(
            IndicatorsTable.is_deleted == False,
            IndicatorValuesTable.is_deleted == False,
        )
        .distinct(IndicatorsTable.id)
        .all()
    )

    if not rows:
        return {}

    grouped: dict[str, dict[str, list[str]]] = {}
    for indicator in rows:
        section_id = _resolve_section_id(indicator.type, indicator.theme)
        theme = (indicator.theme or indicator.type or "Показатели").strip()
        grouped.setdefault(section_id, {}).setdefault(theme, []).append(indicator.name.strip())

    result: dict[str, list[dict]] = {}
    for section_id, themes in grouped.items():
        section_blocks: list[dict] = []
        index = 1
        for theme, names in sorted(themes.items(), key=lambda item: item[0].lower()):
            unique_names = sorted({name for name in names if name}, key=str.lower)
            for name_chunk in _chunk(unique_names, 4):
                if not name_chunk:
                    continue
                block_id = f"{section_id}-{index}"
                section_blocks.append(
                    {
                        "id": block_id,
                        "title": theme,
                        "chartType": "line",
                        "indicators": ",".join(name_chunk),
                    }
                )
                index += 1
        if section_blocks:
            result[section_id] = section_blocks

    if "regional" not in result:
        sample = result.get("s1") or result.get("s5") or []
        if sample:
            result["regional"] = [dict(sample[0], id="regional-1")]

    return result

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
    db_config = _load_json_config(session, "contentBlocks")
    if db_config not in (None, {}, []):
        return db_config
    return _build_content_blocks_from_db(session)


@router.get("/subjectIndicators")
def get_subject_indicators(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "subjectIndicators", [])


@router.get("/objectIndicators")
def get_object_indicators(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "objectIndicators", [])

@router.get("/relationsContentBlocks")
def get_relations_content(session: Session = Depends(get_db)):
    return _get_config_or_empty(session, "relationsContentBlocks", {})
