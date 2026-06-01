"""ОПЦИОНАЛЬНЫЙ модуль: напоминания «напомни через 2 часа ...».

Выключен по умолчанию. Включить: ENABLE_REMINDERS=true в .env.
Нужна таблица reminders (есть в schema.sql).
Планировщик (scheduler.py) раз в минуту проверяет наступившие напоминания.
Подробно — docs/06-add-reminders.md
"""

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from assistant.config import TIMEZONE
from assistant.db import supabase

logger = logging.getLogger(__name__)

PROMPT_ADDON = """\
МОДУЛЬ НАПОМИНАНИЙ включён. если человек говорит «напомни через X / в HH:MM / завтра в ...» —
посчитай точное время от текущего (оно есть выше в системном промпте) и вызови create_reminder
с remind_at в формате ISO (в местном времени человека). коротко подтверди: «напомню тогда-то».
"""

TOOLS = [
    {
        "name": "create_reminder",
        "description": (
            "Создать напоминание. Текущее время есть в системном промпте — "
            "посчитай remind_at = сейчас + интервал. Формат ISO: 2026-01-31T15:30:00."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "remind_at": {"type": "string", "description": "ISO datetime в местном времени"},
                "text": {"type": "string", "description": "Текст напоминания"},
            },
            "required": ["remind_at", "text"],
        },
    },
]


def _create_reminder(data: dict) -> dict:
    try:
        remind_at = datetime.fromisoformat(data["remind_at"])
    except (ValueError, TypeError):
        return {"error": f"неверный формат remind_at: {data.get('remind_at')}"}
    if remind_at.tzinfo is None:
        remind_at = remind_at.replace(tzinfo=TIMEZONE)
    remind_at_utc = remind_at.astimezone(ZoneInfo("UTC"))
    supabase.table("reminders").insert({
        "remind_at": remind_at_utc.isoformat(),
        "text": data["text"],
        "done": False,
    }).execute()
    return {"created": True, "remind_at": data["remind_at"], "text": data["text"]}


HANDLERS = {"create_reminder": _create_reminder}


# ── Используется планировщиком (scheduler.py), не самим Claude ────────
def get_due_reminders() -> list[dict]:
    """Напоминания, время которых наступило (сравнение в UTC)."""
    now = datetime.now(ZoneInfo("UTC")).isoformat()
    return (
        supabase.table("reminders")
        .select("*")
        .eq("done", False)
        .lte("remind_at", now)
        .order("remind_at")
        .execute()
        .data
    )


def mark_reminder_done(reminder_id: int) -> None:
    supabase.table("reminders").update({"done": True}).eq("id", reminder_id).execute()
