"""Базовые инструменты — рефлексии (утро/вечер). Всегда включены.

Это образец того, как устроен инструмент:
  • схема в TOOLS — что ассистент может вызвать и с какими полями
  • функция-обработчик — что реально происходит
  • HANDLERS — связывает имя из схемы с функцией
"""

from datetime import date

from assistant import db

TOOLS = [
    {
        "name": "save_reflection",
        "description": (
            "Сохранить утреннюю или вечернюю рефлексию. "
            "Утро: main_focus (фокус дня), priorities (топ-3 задачи), energy, mood. "
            "Вечер: win (главная победа), day_rating (оценка 1-10), gratitude, mood. "
            "В notes клади полный текст ответа человека."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "time_of_day": {"type": "string", "enum": ["утро", "вечер"]},
                "main_focus": {"type": "string", "description": "Главный фокус дня (утро)"},
                "priorities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Топ-3 приоритетные задачи (утро)",
                },
                "energy": {"type": "integer", "description": "Энергия 1-10"},
                "mood": {"type": "string", "description": "Настроение"},
                "win": {"type": "string", "description": "Главная победа дня (вечер)"},
                "insight": {"type": "string", "description": "Инсайт дня"},
                "gratitude": {"type": "string", "description": "За что благодарна (вечер)"},
                "day_rating": {"type": "integer", "description": "Оценка дня 1-10 (вечер)"},
                "notes": {"type": "string", "description": "Полный текст ответа"},
                "date": {"type": "string", "description": "YYYY-MM-DD (по умолчанию сегодня)"},
            },
            "required": ["time_of_day"],
        },
    },
    {
        "name": "get_reflections",
        "description": (
            "Получить последние рефлексии — для обзоров и вопросов вроде "
            "«какой у меня был фокус сегодня» или «что я планировала»."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 7},
                "time_of_day": {"type": "string", "enum": ["утро", "вечер"]},
            },
        },
    },
]


def _save_reflection(data: dict) -> dict:
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
    return {"saved": True, "time_of_day": data["time_of_day"]}


def _get_reflections(data: dict) -> list[dict]:
    return db.get_reflections(data.get("limit", 7), data.get("time_of_day"))


HANDLERS = {
    "save_reflection": _save_reflection,
    "get_reflections": _get_reflections,
}
