# Урок 4. Чтение почты 📧

**Что добавляем:** бот видит важные непрочитанные письма и может упомянуть их
утром или по запросу («что на почте?»). **Только чтение** — ничего не отправляет
и не удаляет.

Это первый модуль, где нужен Google. Настройка Google делается один раз и потом
переиспользуется в Уроке 5 (календарь). Шагов больше, чем обычно, — иди не спеша.

---

## Часть А. Настроить доступ Google (один раз)

### 1. Создай проект в Google Cloud

1. Зайди на [console.cloud.google.com](https://console.cloud.google.com).
2. Вверху создай новый проект (любое имя).

### 2. Включи Gmail API

Слева **APIs & Services → Library** → найди **Gmail API** → **Enable**.
(Если планируешь Урок 5 — заодно включи и **Google Calendar API**.)

### 3. Настрой экран согласия (OAuth consent screen)

1. **APIs & Services → OAuth consent screen**.
2. Тип — **External**, дальше **Create**.
3. Заполни обязательные поля (имя приложения, твоя почта). Логотип и прочее —
   не нужно.
4. На шаге **Test users** добавь свою Gmail-почту. Это важно: пока приложение
   «в тесте», доступ есть только у добавленных пользователей — этого достаточно,
   публиковать ничего не надо.

### 4. Создай OAuth Client ID

1. **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
2. Тип — **Web application**.
3. В **Authorized redirect URIs** добавь адрес твоего бота + `/google/callback`.
   Где взять адрес: Railway → твой сервис → **Settings → Networking → Generate
   Domain**. Получишь вроде `https://your-app.up.railway.app`. Значит сюда впиши:
   ```
   https://your-app.up.railway.app/google/callback
   ```
4. Нажми **Create**. Google покажет **Client ID** и **Client Secret** — скопируй
   оба.

---

## Часть Б. Включить модуль

Railway → **Variables**, добавь:

```
ENABLE_GMAIL=true
GOOGLE_CLIENT_ID=<твой Client ID>
GOOGLE_CLIENT_SECRET=<твой Client Secret>
GOOGLE_REDIRECT_URI=https://your-app.up.railway.app/google/callback
```

`GOOGLE_REDIRECT_URI` должен **точь-в-точь** совпадать с тем, что ты вписала в
шаге 4. Railway пересоберётся сам.

---

## Часть В. Авторизоваться (один раз)

1. Открой в браузере: `https://your-app.up.railway.app/google/auth`
2. Нажми ссылку, выбери свой Google-аккаунт, разреши доступ.
   (Google может показать «приложение не проверено» — это нормально для теста,
   жми «Дополнительно → перейти».)
3. Увидишь «Готово ✅» — токен сохранён в твою базу и дальше обновляется сам.

---

## Проверь

Напиши боту: «что важного на почте?» — он покажет непрочитанные важные письма
(от кого + тема). Утром тоже может упомянуть их одной строкой.

## Если не работает

- **«Google не авторизован»** → пройди Часть В ещё раз.
- **`redirect_uri_mismatch`** → адрес в Google Cloud и в `GOOGLE_REDIRECT_URI`
  отличаются. Сделай их одинаковыми (включая `https://` и без слэша в конце).
- **`access_denied`** → добавь свою почту в **Test users** (Часть А, шаг 3).

---

→ Дальше: [календарь](05-add-calendar.md) (Google уже настроен — будет быстро) ·
[напоминания](06-add-reminders.md) · [свой инструмент](07-build-your-own-tool.md)
