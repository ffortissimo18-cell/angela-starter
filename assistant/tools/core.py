"""Базовые инструменты — рефлексии (утро/вечер). Всегда включены."""

from datetime import date

from assistant import db

TOOLS = [
    {
        "name": "save_reflection",
        "description": "Сохранить утреннюю или вечернюю рефлексию.",
        "input_schema": {
            "type": "object",
            "properties": {
                "time_of_day": {"type": "string", "enum": ["утро", "вечер"]},
                "main_focus": {"type": "string"},
                "priorities": {"type": "array", "items": {"type": "string"}},
                "energy": {"type": "integer"},
                "mood": {"type": "string"},
                "win": {"type": "string"},
                "insight": {"type": "string"},
                "gratitude": {"type": "string"},
                "day_rating": {"type": "integer"},
                "notes": {"type": "string"},
                "date": {"type": "string"},
            },
            "required": ["time_of_day"],
        },
    },
    {
        "name": "get_reflections",
        "description": "Получить последние рефлексии.",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 7},
                "time_of_day": {"type": "string", "enum": ["утро", "вечер"]},
            },
        },
    },
]


def _save_reflection(data):
    ref_date = date.fromisoformat(data["date"]) if data.get("date") else None
    db.save_reflection(
        time_of_day=data["time_of_day"],
        main_focus=data.get("main_focus"),
        priorities=data.get("priorities"),
        energy=data.get("energy"),
        mood=data.get("mood"),
        win=data.get("win"),
        insight=data.get("insight"),
        gratitude=data.get("gratitude"),
        day_rating=data.get("day_rating"),
        notes=data.get("notes"),
        ref_date=ref_date,
    )
    try:
        from assistant import notion_sync
        notion_sync.push_reflection(
            time_of_day=data["time_of_day"],
            main_focus=data.get("main_focus"),
            priorities=data.get("priorities"),
            energy=data.get("energy"),
            mood=data.get("mood"),
            win=data.get("win"),
            insight=data.get("insight"),
            gratitude=data.get("gratitude"),
            day_rating=data.get("day_rating"),
            notes=data.get("notes"),
            ref_date=ref_date,
        )
    except Exception:
        pass
    return {"saved": True, "time_of_day": data["time_of_day"]}


def _get_reflections(data):
    return db.get_reflections(data.get("limit", 7), data.get("time_of_day"))


HANDLERS = {
    "save_reflection": _save_reflection,
    "get_reflections": _get_reflections,
}
