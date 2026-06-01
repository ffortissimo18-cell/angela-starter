"""ОПЦИОНАЛЬНЫЙ модуль: чтение Gmail (только чтение, ничего не отправляет).

Выключен по умолчанию. Включить: ENABLE_GMAIL=true в .env + ключи Google.
Сначала пройди общий шаг авторизации Google. Подробно — docs/04-add-gmail.md
"""

import logging

import httpx

from assistant.google_auth import get_access_token

logger = logging.getLogger(__name__)
API = "https://www.googleapis.com/gmail/v1"

PROMPT_ADDON = """\
МОДУЛЬ ПОЧТЫ включён (только чтение). в утреннем чекине, если уместно, можешь одной строкой
упомянуть важные непрочитанные письма. отдельно показывай почту, только когда просят
(«что на почте», «есть важные письма»). не дёргай почту в каждом сообщении.
"""

TOOLS = [
    {
        "name": "gmail_unread",
        "description": "Непрочитанные письма из Gmail (от кого + тема). Покажи кратко.",
        "input_schema": {
            "type": "object",
            "properties": {"max_results": {"type": "integer", "default": 10}},
        },
    },
    {
        "name": "gmail_important",
        "description": "Только важные/помеченные непрочитанные письма.",
        "input_schema": {
            "type": "object",
            "properties": {"max_results": {"type": "integer", "default": 5}},
        },
    },
]


def _header(headers: list[dict], name: str) -> str:
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def _list(query: str, max_results: int) -> list[dict]:
    token = get_access_token()
    if not token:
        return [{"error": "Google не авторизован — открой /google/auth у бота"}]
    auth = {"Authorization": f"Bearer {token}"}
    try:
        resp = httpx.get(f"{API}/users/me/messages",
                         headers=auth, params={"q": query, "maxResults": max_results}, timeout=15)
        resp.raise_for_status()
        messages = resp.json().get("messages", [])
        out = []
        for m in messages:
            d = httpx.get(f"{API}/users/me/messages/{m['id']}", headers=auth, params={
                "format": "metadata", "metadataHeaders": ["From", "Subject"],
            }, timeout=15).json()
            headers = d.get("payload", {}).get("headers", [])
            out.append({
                "from": _header(headers, "From"),
                "subject": _header(headers, "Subject"),
                "snippet": d.get("snippet", ""),
            })
        return out
    except Exception as exc:
        logger.exception("ошибка Gmail")
        return [{"error": str(exc)}]


def _gmail_unread(data: dict) -> list[dict]:
    return _list("is:unread", data.get("max_results", 10))


def _gmail_important(data: dict) -> list[dict]:
    return _list("is:unread (is:important OR is:starred)", data.get("max_results", 5))


HANDLERS = {"gmail_unread": _gmail_unread, "gmail_important": _gmail_important}
