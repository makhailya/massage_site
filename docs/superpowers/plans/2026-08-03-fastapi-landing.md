# FastAPI Landing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заменить Django-монолит на минимальный FastAPI-лендинг с формой заявки в Telegram.

**Architecture:** FastAPI раздаёт статический `index.html` и обрабатывает единственный endpoint `POST /api/lead`, который через Telegram Bot API отправляет заявку владельцу. Никакой БД, авторизации или шаблонов. Инфраструктура: docker-compose с сервисами `web` (uvicorn) и `cloudflared`, CI/CD через GitHub Actions.

**Tech Stack:** Python 3.13+, FastAPI, uvicorn, httpx, pytest, ruff, bandit, docker, docker-compose.

---

## Файловая структура

Новые файлы:
- `app.py` — FastAPI-приложение (index + `/api/lead` + rate-limit)
- `static/index.html` — одностраничный лендинг
- `static/style.css` — стили (тёмный editorial, изумрудный акцент)
- `static/app.js` — отправка формы через `fetch`
- `requirements.txt` — зависимости
- `requirements-dev.txt` — dev-зависимости
- `Dockerfile` — перезаписать (python:3.13-slim + uvicorn)
- `docker-compose.yml` — перезаписать (web + cloudflared)
- `.env.example` — пример переменных
- `tests/test_app.py` — тесты
- `docs/superpowers/plans/` — этот план

Удаляемые файлы/папки:
- `booking/`, `services/`, `users/`, `config/`, `templates/`, `nginx/`
- `manage.py`, `main.py`, `db.sqlite3`, `pytest.ini`, `poetry.lock`, `staticfiles/`
- Перезаписать: `pyproject.toml`, `.github/workflows/deploy.yml`, `.gitignore`, `README.md`

---

### Task 1: Зависимости и конфиг

**Files:**
- Create: `requirements.txt`
- Create: `requirements-dev.txt`
- Overwrite: `pyproject.toml`

- [ ] **Step 1: Написать requirements.txt**

```txt
fastapi>=0.115,<1.0
uvicorn[standard]>=0.34,<1.0
httpx>=0.28,<1.0
```

- [ ] **Step 2: Написать requirements-dev.txt**

```txt
-r requirements.txt
pytest>=8.0,<10.0
ruff>=0.15,<0.16
bandit>=1.9,<2.0
```

- [ ] **Step 3: Перезаписать pyproject.toml**

```toml
[tool.ruff]
line-length = 88
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

- [ ] **Step 4: Установить зависимости в venv**

Run: `uv pip install -r requirements-dev.txt` (в активном venv, либо через `--python .venv/bin/python`)

Expected: успешная установка fastapi, uvicorn, httpx, pytest, ruff, bandit

---

### Task 2: FastAPI приложение — GET /

**Files:**
- Create: `app.py`
- Create: `tests/test_app.py`

- [ ] **Step 1: Написать падающий тест**

```python
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `pytest tests/test_app.py::test_home_page -v`
Expected: FAIL с `ModuleNotFoundError: No module named 'app'`

- [ ] **Step 3: Написать минимальный app.py**

```python
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")
```

- [ ] **Step 4: Создать минимальный static/index.html**

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Массаж Илья Маханек</title>
</head>
<body>
    <h1>Илья Маханек</h1>
</body>
</html>
```

- [ ] **Step 5: Запустить тест — убедиться, что проходит**

Run: `pytest tests/test_app.py::test_home_page -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add app.py tests/test_app.py static/index.html
git commit -m "feat: add FastAPI app serving landing page"
```

---

### Task 3: POST /api/lead — валидация и Telegram

**Files:**
- Modify: `app.py`
- Modify: `tests/test_app.py`

- [ ] **Step 1: Написать падающие тесты**

```python
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_valid_lead_sends_telegram(monkeypatch):
    sent = []

    async def fake_send(name, phone):
        sent.append((name, phone))

    monkeypatch.setattr("app.send_telegram_message", fake_send)

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    assert sent == [("Иван", "+7 (912) 600-51-61")]


def test_invalid_phone_rejected():
    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "abc"},
    )
    assert response.status_code == 422


def test_missing_fields_rejected():
    response = client.post("/api/lead", json={"name": "Иван"})
    assert response.status_code == 422


def test_telegram_error_returns_502(monkeypatch):
    async def failing_send(name, phone):
        raise RuntimeError("telegram down")

    monkeypatch.setattr("app.send_telegram_message", failing_send)

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 502
```

- [ ] **Step 2: Запустить тесты — убедиться, что падают**

Run: `pytest tests/test_app.py -v`
Expected: FAIL с `AttributeError: module 'app' has no attribute 'send_telegram_message'`

- [ ] **Step 3: Реализовать endpoint и валидацию в app.py**

```python
import os
import re
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class LeadIn(BaseModel):
    name: str
    phone: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        v = v.strip()
        if not 1 <= len(v) <= 100:
            raise ValueError("Имя должно быть от 1 до 100 символов")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        v = v.strip()
        if not re.fullmatch(r"[0-9+()\- ]+", v):
            raise ValueError("Телефон содержит недопустимые символы")
        digits = re.sub(r"\D", "", v)
        if not 10 <= len(digits) <= 15:
            raise ValueError("Телефон должен содержать 10–15 цифр")
        return v


async def send_telegram_message(name: str, phone: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("Telegram не настроен: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID")

    text = f"📩 Новая заявка\n👤 {name}\n📞 {phone}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10.0,
        )
    if resp.status_code != 200:
        raise RuntimeError(f"Telegram API error: {resp.status_code}")


@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.post("/api/lead")
async def create_lead(lead: LeadIn):
    try:
        await send_telegram_message(lead.name, lead.phone)
    except RuntimeError:
        raise HTTPException(status_code=502, detail="Не удалось отправить заявку")
    return {"ok": True}
```

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `pytest tests/test_app.py -v`
Expected: PASS (все 5 тестов)

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "feat: add lead endpoint with Telegram notification"
```

---

### Task 4: Rate-limit на /api/lead

**Files:**
- Modify: `app.py`
- Modify: `tests/test_app.py`

- [ ] **Step 1: Написать падающий тест**

```python
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_rate_limit_blocks_after_limit(monkeypatch):
    async def fake_send(name, phone):
        pass

    monkeypatch.setattr("app.send_telegram_message", fake_send)

    for _ in range(3):
        response = client.post(
            "/api/lead",
            json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
        )
        assert response.status_code == 200

    response = client.post(
        "/api/lead",
        json={"name": "Иван", "phone": "+7 (912) 600-51-61"},
    )
    assert response.status_code == 429
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `pytest tests/test_app.py::test_rate_limit_blocks_after_limit -v`
Expected: FAIL (4-й запрос вернёт 200)

- [ ] **Step 3: Добавить rate-limit в app.py**

В начале файла добавить импорт и состояние:

```python
import os
import re
import time
from collections import defaultdict
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

BASE_DIR = Path(__file__).resolve().parent

RATE_LIMIT_PER_MINUTE = 3
_requests_log = defaultdict(list)

app = FastAPI()
```

Заменить сигнатуру `create_lead`:

```python
@app.post("/api/lead")
async def create_lead(lead: LeadIn, request: Request):
    client_ip = request.client.host if request.client else "unknown"

    now = time.monotonic()
    cutoff = now - 60
    _requests_log[client_ip] = [t for t in _requests_log[client_ip] if t > cutoff]
    if len(_requests_log[client_ip]) >= RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Слишком много заявок, попробуйте позже")
    _requests_log[client_ip].append(now)

    try:
        await send_telegram_message(lead.name, lead.phone)
    except RuntimeError:
        raise HTTPException(status_code=502, detail="Не удалось отправить заявку")
    return {"ok": True}
```

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `pytest tests/test_app.py -v`
Expected: PASS (все тесты)

- [ ] **Step 5: Commit**

```bash
git add app.py tests/test_app.py
git commit -m "feat: add rate limiting to lead endpoint"
```

---

### Task 5: Полный лендинг (index.html, style.css, app.js)

**Files:**
- Modify: `static/index.html`
- Create: `static/style.css`
- Create: `static/app.js`

- [ ] **Step 1: Написать static/index.html**

Тёмный editorial, секции: Hero (фото + имя + подзаголовок), Обо мне, Услуги, Контакты + форма.

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Массаж Илья Маханек — Верхняя Пышма</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="nav">
        <span class="logo">ИМ</span>
        <div class="nav-links">
            <a href="#about">Обо мне</a>
            <a href="#services">Услуги</a>
            <a href="#contact">Контакты</a>
        </div>
    </nav>

    <header class="hero" id="hero">
        <div class="hero-text">
            <p class="eyebrow">Массаж · Верхняя Пышма</p>
            <h1>Илья<br>Маханек</h1>
            <p class="hero-sub">Массаж на дому и с выездом. Снимаю напряжение, возвращаю лёгкость и энергию.</p>
            <div class="hero-actions">
                <a href="#contact" class="btn btn-primary">Записаться</a>
                <a href="tel:+79126005161" class="btn btn-ghost">Позвонить</a>
            </div>
        </div>
        <div class="hero-photo">
            <div class="photo-placeholder">ИМ</div>
        </div>
    </header>

    <section class="section" id="about">
        <p class="eyebrow">Обо мне</p>
        <h2>Ваше тело скажет спасибо</h2>
        <p class="section-text">Профессиональный массаж для тех, кто много работает и мало отдыхает. Работаю с мышцами бережно и эффективно, подбираю технику под ваши задачи.</p>
    </section>

    <section class="section" id="services">
        <p class="eyebrow">Услуги и цены</p>
        <h2>Прайс</h2>
        <div class="menu">
            <div class="menu-item">
                <div class="menu-info">
                    <h3>Оздоровительный массаж</h3>
                    <p>Классический массаж для снятия напряжения и улучшения самочувствия</p>
                </div>
                <div class="menu-meta">
                    <span class="duration">40 мин</span>
                    <span class="price">1 500 ₽</span>
                </div>
            </div>
            <div class="menu-item">
                <div class="menu-info">
                    <h3>Релакс-массаж</h3>
                    <p>Глубокая релаксация, мягкая работа с телом, снимает стресс</p>
                </div>
                <div class="menu-meta">
                    <span class="duration">60 мин</span>
                    <span class="price">2 000 ₽</span>
                </div>
            </div>
            <div class="menu-item">
                <div class="menu-info">
                    <h3>Массаж с выездом на дом</h3>
                    <p>Полноценный сеанс в комфортной обстановке вашего дома</p>
                </div>
                <div class="menu-meta">
                    <span class="duration">90 мин</span>
                    <span class="price">2 500 ₽</span>
                </div>
            </div>
        </div>
    </section>

    <section class="section" id="contact">
        <p class="eyebrow">Контакты</p>
        <h2>Запишитесь на сеанс</h2>
        <div class="contact-grid">
            <div class="contact-links">
                <a class="contact-link" href="tel:+79126005161">📞 +7 912 600-51-61</a>
                <a class="contact-link" href="https://wa.me/79126005161" target="_blank">💬 WhatsApp</a>
                <a class="contact-link" href="https://t.me/makhailya" target="_blank">✈️ Telegram</a>
                <a class="contact-link" href="https://max.ru/makhailya" target="_blank">💠 MAX</a>
            </div>
            <form id="lead-form" class="lead-form">
                <label>
                    Ваше имя
                    <input type="text" id="name" name="name" maxlength="100" required placeholder="Иван">
                </label>
                <label>
                    Телефон
                    <input type="tel" id="phone" name="phone" required placeholder="+7 (912) 000-00-00">
                </label>
                <button type="submit" class="btn btn-primary">Отправить заявку</button>
                <p id="form-status" class="form-status"></p>
            </form>
            <div id="form-success" class="form-success hidden">
                <h3>Спасибо!</h3>
                <p>Скоро свяжусь с вами.</p>
                <a href="https://t.me/makhailya" target="_blank" class="btn btn-primary">Открыть Telegram</a>
            </div>
        </div>
    </section>

    <footer class="footer">
        <p>© 2026 Илья Маханек · Верхняя Пышма</p>
    </footer>

    <script src="/static/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Написать static/style.css**

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

:root {
    --bg: #0e0e0e;
    --text: #e8e0d5;
    --muted: #9a9388;
    --accent: #10b981;
    --accent-dark: #0d9669;
    --line: #2a2a2a;
    --serif: 'Playfair Display', Georgia, serif;
    --sans: 'Inter', Helvetica, Arial, sans-serif;
}

html { scroll-behavior: smooth; }

body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--sans);
    font-weight: 300;
    line-height: 1.6;
}

.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 48px;
    border-bottom: 1px solid var(--line);
}

.logo {
    font-family: var(--serif);
    font-size: 20px;
    letter-spacing: 2px;
}

.nav-links a {
    color: var(--muted);
    text-decoration: none;
    margin-left: 32px;
    font-size: 14px;
    letter-spacing: 1px;
    transition: color 0.2s;
}

.nav-links a:hover { color: var(--accent); }

.hero {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 48px;
    align-items: center;
    padding: 80px 48px;
    max-width: 1100px;
    margin: 0 auto;
}

.eyebrow {
    color: var(--accent);
    letter-spacing: 4px;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero h1 {
    font-family: var(--serif);
    font-size: 72px;
    font-weight: 600;
    line-height: 1.05;
    margin-bottom: 24px;
}

.hero-sub {
    color: var(--muted);
    font-size: 18px;
    max-width: 480px;
    margin-bottom: 32px;
}

.hero-actions { display: flex; gap: 16px; }

.btn {
    display: inline-block;
    padding: 14px 28px;
    font-size: 15px;
    font-family: var(--sans);
    text-decoration: none;
    border: 1px solid transparent;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 1px;
}

.btn-primary {
    background: var(--accent);
    color: #0a0a0a;
    font-weight: 500;
}

.btn-primary:hover { background: var(--accent-dark); }

.btn-ghost {
    border-color: var(--line);
    color: var(--text);
    background: transparent;
}

.btn-ghost:hover { border-color: var(--accent); color: var(--accent); }

.photo-placeholder {
    width: 100%;
    aspect-ratio: 4 / 5;
    background: linear-gradient(135deg, #1a3a2e, #0e0e0e);
    border: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--serif);
    font-size: 64px;
    color: var(--accent);
}

.section {
    max-width: 900px;
    margin: 0 auto;
    padding: 80px 48px;
    border-top: 1px solid var(--line);
}

.section h2 {
    font-family: var(--serif);
    font-size: 40px;
    font-weight: 400;
    margin-bottom: 24px;
}

.section-text { color: var(--muted); font-size: 17px; max-width: 640px; }

.menu { margin-top: 32px; }

.menu-item {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 24px;
    padding: 24px 0;
    border-bottom: 1px solid var(--line);
}

.menu-item:last-child { border-bottom: none; }

.menu-info h3 { font-family: var(--serif); font-size: 22px; font-weight: 400; margin-bottom: 6px; }

.menu-info p { color: var(--muted); font-size: 14px; }

.menu-meta { display: flex; gap: 24px; align-items: baseline; white-space: nowrap; }

.duration { color: var(--muted); font-size: 14px; }

.price { color: var(--accent); font-family: var(--serif); font-size: 24px; }

.contact-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; margin-top: 32px; }

.contact-links { display: flex; flex-direction: column; gap: 16px; }

.contact-link {
    color: var(--text);
    text-decoration: none;
    font-size: 18px;
    border-bottom: 1px solid var(--line);
    padding-bottom: 12px;
    transition: color 0.2s;
}

.contact-link:hover { color: var(--accent); }

.lead-form { display: flex; flex-direction: column; gap: 16px; }

.lead-form label { display: flex; flex-direction: column; gap: 6px; color: var(--muted); font-size: 13px; letter-spacing: 1px; }

.lead-form input {
    background: #171717;
    border: 1px solid var(--line);
    color: var(--text);
    padding: 12px 16px;
    font-size: 16px;
    font-family: var(--sans);
    outline: none;
    transition: border-color 0.2s;
}

.lead-form input:focus { border-color: var(--accent); }

.lead-form input::placeholder { color: #5c584f; }

.form-status { color: #ef4444; font-size: 14px; min-height: 20px; }

.form-success { display: flex; flex-direction: column; gap: 16px; align-items: flex-start; }

.form-success h3 { font-family: var(--serif); font-size: 28px; font-weight: 400; }

.form-success p { color: var(--muted); }

.hidden { display: none; }

.footer {
    text-align: center;
    padding: 32px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 13px;
}

@media (max-width: 768px) {
    .hero { grid-template-columns: 1fr; padding: 48px 24px; }
    .hero h1 { font-size: 48px; }
    .section { padding: 48px 24px; }
    .menu-item { flex-direction: column; gap: 8px; }
    .contact-grid { grid-template-columns: 1fr; }
    .nav { padding: 20px 24px; }
    .nav-links a { margin-left: 20px; }
}
```

- [ ] **Step 3: Написать static/app.js**

```javascript
const form = document.getElementById('lead-form');
const status = document.getElementById('form-status');
const success = document.getElementById('form-success');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    status.textContent = '';

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();

    try {
        const response = await fetch('/api/lead', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone }),
        });

        if (response.ok) {
            form.classList.add('hidden');
            success.classList.remove('hidden');
        } else {
            const data = await response.json().catch(() => ({}));
            status.textContent = data.detail || 'Что-то пошло не так, попробуйте ещё раз.';
        }
    } catch {
        status.textContent = 'Нет соединения. Попробуйте ещё раз.';
    }
});
```

- [ ] **Step 4: Проверить GET / тест**

Run: `pytest tests/test_app.py::test_home_page -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add static/index.html static/style.css static/app.js
git commit -m "feat: add landing page with contact form"
```

---

### Task 6: Dockerfile и docker-compose

**Files:**
- Overwrite: `Dockerfile`
- Overwrite: `docker-compose.yml`

- [ ] **Step 1: Перезаписать Dockerfile**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Перезаписать docker-compose.yml**

```yaml
services:
  web:
    build: .
    env_file: .env
    restart: unless-stopped
    networks:
      - app-network

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflare-tunnel
    restart: unless-stopped
    command: tunnel --no-autoupdate run --token ${CLOUDFLARED_TUNNEL_TOKEN}
    env_file: .env
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

- [ ] **Step 3: Создать .env.example**

```dotenv
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
CLOUDFLARED_TUNNEL_TOKEN=
```

- [ ] **Step 4: Commit**

```bash
git add Dockerfile docker-compose.yml .env.example
git commit -m "chore: simplify docker setup for FastAPI"
```

---

### Task 7: Обновить CI/CD

**Files:**
- Overwrite: `.github/workflows/deploy.yml`

- [ ] **Step 1: Перезаписать deploy.yml**

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: self-hosted
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.SERVER_HOST }} >> ~/.ssh/known_hosts

      - name: Lint & Security check
        run: |
          pip install --user ruff bandit
          python -m ruff check .
          python -m bandit -r . -x .venv,__pycache__,tests,static

      - name: Deploy to server
        run: |
          ssh -i ~/.ssh/deploy_key ${{ secrets.SERVER_USER }}@${{ secrets.SERVER_HOST }} << 'EOF'
            cd /opt/massage_site
            git pull origin main
            docker compose up --build -d
            docker compose restart web
            echo "✅ Деплой завершён!"
          EOF

      - name: Clean up SSH key
        if: always()
        run: rm -f ~/.ssh/deploy_key
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: update deploy workflow for FastAPI"
```

---

### Task 8: Удалить Django-код

**Files:**
- Delete: `booking/`, `services/`, `users/`, `config/`, `templates/`, `nginx/`, `staticfiles/`
- Delete: `manage.py`, `main.py`, `db.sqlite3`, `pytest.ini`, `poetry.lock`

- [ ] **Step 1: Удалить файлы**

```bash
git rm -r booking services users config templates nginx staticfiles
git rm manage.py main.py db.sqlite3 pytest.ini poetry.lock
```

- [ ] **Step 2: Убедиться, что тесты всё ещё проходят**

Run: `pytest tests/ -v`
Expected: PASS (все тесты)

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove Django app"
```

---

### Task 9: Обновить README и .gitignore

**Files:**
- Overwrite: `README.md`
- Modify: `.gitignore`

- [ ] **Step 1: Обновить .gitignore**

```
.env
.venv
__pycache__
*.pyc
*.sqlite3
.idea
.DS_Store
.coverage
.pytest_cache
.ruff_cache
.claude/
```

- [ ] **Step 2: Написать README.md**

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
git add README.md .gitignore
git commit -m "docs: update README and gitignore"
```

---

### Task 10: Финальная проверка

- [ ] **Step 1: Прогнать все тесты**

Run: `pytest tests/ -v`
Expected: PASS

- [ ] **Step 2: Проверить lint**

Run: `python -m ruff check .`
Expected: no errors

- [ ] **Step 3: Проверить bandit**

Run: `python -m bandit -r . -x .venv,__pycache__,tests,static`
Expected: no high severity issues

- [ ] **Step 4: Проверить запуск локально**

Run: `uvicorn app:app --port 8000` и открыть http://localhost:8000
Expected: лендинг отображается, форма работает (502 без настроенного Telegram — ок)

- [ ] **Step 5: Проверить git status чистый**

Run: `git status`
Expected: чистое рабочее дерево
