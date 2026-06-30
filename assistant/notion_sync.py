"""Опционально дублирует рефлексии в Notion-базу.

Если в .env заданы NOTION_TOKEN и NOTION_DATABASE_ID — после сохранения
рефлексии в Supabase бот тихо создаёт страницу в Notion. Если ключей нет
или Notion недоступен — просто молча пропускаем (Supabase это не ломает).
"""

from __future__ import annotations

import logging
import os
from datetime import date as date_cls

import httpx

logger = logging.getLogger(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
NOTION_VERSION = "2022-06-28"


def enabled() -> bool:
    return bool(NOTION_TOKEN and NOTION_DATABASE_ID)


def _rich_text(value: str | None) -> list[dict]:
    if not value:
        return []
    return [{"type": "text", "text": {"content": str(value)[:2000]}}]


def _number(value) -> dict | None:
    if value is None:
        return None
    try:
        return {"number": float(value)}
    except (TypeError, ValueError):
        return None


def push_reflection(
    *,
    time_of_day: str,
    main_focus: str | None = None,
    priorities: list[str] | None = None,
    energy: int | None = None,
    mood: str | None = None,
    win: str | None = None,
    insight: str | None = None,
    gratitude: str | None = None,
    day_rating: int | None = None,
    notes: str | None = None,
    ref_date: date_cls | None = None,
) -> None:
    """Создать страницу в Notion с полями рефлексии. Best-effort, не бросает."""
    if not enabled():
        return

    day = (ref_date or date_cls.today()).isoformat()
    title = f"{day} · {time_of_day}"
    prio_text = "\n".join(f"• {p}" for p in priorities) if priorities else None

    properties: dict = {
        "Date": {"title": _rich_text(title)},
        "Day": {"date": {"start": day}},
        "Time of day": {"select": {"name": time_of_day}},
    }
    text_fields = {
        "Main focus": main_focus,
        "Priorities": prio_text,
        "Win": win,
        "Mood": mood,
        "Gratitude": gratitude,
        "Insight": insight,
        "Notes": notes,
    }
    for key, val in text_fields.items():
        rt = _rich_text(val)
        if rt:
            properties[key] = {"rich_text": rt}
    for key, val in (("Energy", energy), ("Day rating", day_rating)):
        n = _number(val)
        if n is not None:
            properties[key] = n

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": properties,
    }
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }

    try:
        r = httpx.post(
            "https://api.notion.com/v1/pages",
            json=payload,
            headers=headers,
            timeout=15.0,
        )
        if r.status_code >= 300:
            logger.warning("notion push failed %s: %s", r.status_code, r.text[:300])
    except Exception:
        logger.exception("notion push error") 
