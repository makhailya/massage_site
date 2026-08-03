# FastAPI-лендинг массажиста — дизайн

Дата: 2026-08-03
Статус: approved

## Цель

Полностью заменить Django-монолит на минимальный FastAPI-лендинг с одной формой
заявки в Telegram. Убрать БД, авторизацию, админку, шаблоны. Цель — максимально
простой одностраничник, который продаёт услуги массажа и отправляет заявки
владельцу в Telegram.

## Текущий стек (что заменяем)

- Django 6 + серверные шаблоны, 3 приложения (`services`, `booking`, `users`)
- PostgreSQL 15 (docker-compose `db`), ORM, миграции
- nginx + staticfiles, cloudflared-туннель
- GitHub Actions self-hosted деплой (ruff + bandit)
- pytest + pytest-django

## Целевой стек

- **FastAPI + uvicorn** — единственный бэкенд-сервис
- Статический фронтенд: `index.html`, `style.css`, `app.js` в `static/`
- **Без БД, без ORM, без auth, без Jinja**
- Telegram Bot API для доставки заявок
- docker-compose: только `web` + `cloudflared`
- CI/CD: ruff + bandit → pull → build → up

## Архитектура

```
static/                       index.html, style.css, app.js
app.py                        FastAPI: GET / → index.html; POST /api/lead
docker-compose.yml            web (uvicorn :8000) + cloudflared
Dockerfile                    python:3.13-slim + uvicorn
.env                          TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (не в git)
.github/workflows/deploy.yml  CI/CD остаётся
```

### Backend (`app.py`)

- `StaticFiles` отдаёт `/static/*`; `GET /` рендерит `static/index.html`
- `POST /api/lead`:
  - Pydantic-схема `LeadIn(name: str, phone: str)`
  - Валидация: имя 1–100 символов; телефон — только цифры, `+ - ( )` и пробелы,
    10–15 цифр
  - Отправка `httpx.post` в Telegram Bot API `sendMessage`:
    `📩 Новая заявка\n👤 {name}\n📞 {phone}`
  - Ответ `200 {"ok": true}`; `502` при ошибке Telegram; `422` при невалидных данных
  - Rate-limit в памяти: max 3 запроса/мин с одного IP → `429`

### Frontend (тёмный editorial, изумрудный акцент)

- Фон `#0e0e0e`, текст `#e8e0d5`, акцент `#10b981`
- Hero: фото + «Илья Маханек» крупным серифным шрифтом (Playfair Display) +
  «Массаж на дому и с выездом · Верхняя Пышма» + кнопки «Записаться» / «Позвонить»
- Обо мне: короткий блок
- Услуги — «меню» списком с тонкими разделителями
- Контакты + форма «Имя / Телефон»; после отправки «Спасибо!» + кнопка
  «Открыть Telegram» (`https://t.me/makhailya`)
- Мессенджеры: телефон +7 912 600-51-61, WhatsApp, Telegram, MAX

### Контент

| Услуга | Длительность | Цена |
|---|---|---|
| Оздоровительный массаж | 40 мин | 1500 ₽ |
| Релакс-массаж | 60 мин | 2000 ₽ |
| Массаж с выездом на дом | 90 мин | 2500 ₽ |

### Поток заявки

1. Пользователь заполняет имя/телефон → JS `fetch POST /api/lead`
2. FastAPI валидирует, шлёт сообщение в Telegram боту
3. Клиент видит «Спасибо!» + кнопку «Открыть Telegram»
4. Секреты — в `.env` (bot token, chat_id), не в git

## Инфраструктура

- `docker-compose.yml`: сервисы `web` (build, uvicorn :8000, `env_file: .env`) и
  `cloudflared`; удалить `db`, `nginx`, `static_volume`
- Удалить Django-код: `booking/`, `services/`, `users/`, `config/`, `templates/`,
  `manage.py`, `db.sqlite3`, `nginx/`, старые миграции и тесты (остаются в git-истории)
- Новый минимальный `Dockerfile` (python:3.13-slim + uvicorn, без poetry)
- `deploy.yml`: ruff + bandit → `git pull` → `docker compose up --build -d`;
  убрать `migrate` и `collectstatic`

## Тестирование

- `pytest` + FastAPI `TestClient`:
  - `GET /` → 200
  - `POST /api/lead` валидный → 200 (мок Telegram)
  - `POST /api/lead` невалидный телефон → 422
  - rate-limit превышен → 429
  - ошибка Telegram → 502
- ruff + bandit в CI

## За рамками

- Регистрация/логин, личный кабинет, админка
- БД и история заявок
- Несколько страниц, блог
- Оплата онлайн
