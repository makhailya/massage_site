# Массаж Илья Маханек — лендинг

Одностраничный сайт массажиста на FastAPI. Форма заявки отправляет
уведомление владельцу в Telegram.

## Стек
- FastAPI + uvicorn
- Статический HTML/CSS/JS
- Telegram Bot API для уведомлений

## Локальный запуск
```bash
uv pip install -r requirements-dev.txt
uvicorn app:app --reload
```

Открыть http://localhost:8000

## Тесты
```bash
pytest
```

## Переменные окружения (.env)
| Переменная | Описание |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен бота из @BotFather |
| `TELEGRAM_CHAT_ID` | ID вашего чата для уведомлений |
| `CLOUDFLARED_TUNNEL_TOKEN` | Токен туннеля Cloudflare |

## Деплой
Пуш в ветку `main` запускает GitHub Actions (self-hosted runner):
ruff + bandit → `docker compose up --build -d` на сервере.
