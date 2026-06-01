# Angela Starter 🌿

A personal AI assistant that lives in **Telegram** and checks in with you every
morning and evening. Built on Claude. Fork it, make it yours, extend it lesson
by lesson.

> Russian-first: the bot speaks Russian out of the box and the step-by-step
> lessons are in Russian (`docs/`). Everything is easy to translate — the
> personality lives in one file (`assistant/prompts.py`).

---

## What it does out of the box

- **🌅 Morning check-in** — asks for your focus and top-3 priorities for the day
- **🌙 Evening check-in** — asks what you got done and your win of the day
- **💬 Just talk** — chat any time; it remembers your recent conversation
- Saves your reflections so you can look back

That's the whole core. No email, no calendar, no clutter — until *you* add it.

## Add more, one lesson at a time

Each capability is an optional module you switch on by following a short lesson:

| Lesson | What you add |
|--------|--------------|
| `docs/03-add-cycle.md` | 🌙 Cycle & energy by phase (femtech) |
| `docs/04-add-gmail.md` | 📧 Read your important email |
| `docs/05-add-calendar.md` | 📅 Google Calendar (read + create events) |
| `docs/06-add-reminders.md` | ⏰ Reminders + weekly review |
| `docs/07-build-your-own-tool.md` | 🛠 Write your own tool from scratch |

## Quick start — two ways

**With Claude Code (interactive):** clone or fork this repo, open it in
[Claude Code](https://claude.ai/code), and type "начнём" (or "let's start").
Claude reads `CLAUDE.md` and walks you through every step — asking your name,
schedule, preferred tone, getting the API keys — and edits the files itself.
No reading docs required.

**Manual (read the lessons yourself):**
👉 [`docs/01-setup.md`](docs/01-setup.md) (≈30 minutes, no coding required)

Then make it speak in your voice: [`docs/02-make-it-yours.md`](docs/02-make-it-yours.md)

## Tech stack

Python · [Claude API](https://www.anthropic.com) · [python-telegram-bot](https://python-telegram-bot.org) ·
[Supabase](https://supabase.com) · [Railway](https://railway.app)

## Structure

```
assistant/            # the bot
  prompts.py          # ← the ONLY file you customize (name, tone, check-ins)
  config.py           # reads settings from environment variables
  bot.py              # Telegram handlers
  agent.py            # the Claude brain (tool-use loop)
  scheduler.py        # morning / evening / weekly check-ins
  db.py               # Supabase (memory + reflections)
  tools/              # capabilities — core always on, the rest optional
docs/                 # the lessons (Russian)
schema.sql            # database tables (run once in Supabase)
.env.example          # all settings, explained
```

## License

MIT © 2026 Kate Andreeva. Use it, fork it, build your own assistant on top.
