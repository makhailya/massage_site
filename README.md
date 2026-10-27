# Илья Маханек — массаж · Верхняя Пышма

Одностраничный лендинг массажиста. Основная версия — **статический сайт**
(HTML5, CSS3, Vanilla JS) без сборки, backend и базы данных. Публикуется на
GitHub Pages.

В репозитории также сохранена прежняя версия на FastAPI (`app.py` + `static/`)
с формой заявки в Telegram. Она не используется GitHub Pages и остаётся
опциональной.

## Структура

```
index.html              главная страница для GitHub Pages
css/style.css           стили
js/script.js            анимации появления (GSAP + ScrollTrigger)
assets/images/hero.jpg  портрет
assets/images/favicon.svg
.nojekyll               отключает обработку Jekyll на GitHub Pages
static/                 прежняя версия, которую раздаёт FastAPI
app.py                  FastAPI: POST /api/lead → Telegram
```

## Локальный запуск

Статическая версия (рекомендуется):

```bash
python3 -m http.server 8000
```

Открыть <http://localhost:8000/>. Файл `index.html` также открывается напрямую,
но для загрузки шрифтов и GSAP нужен интернет.

FastAPI-версия (опционально, нужны Python и `.env`):

```bash
uv pip install -r requirements-dev.txt
uvicorn app:app --reload
```

Открыть <http://localhost:8000>. Форма на этой версии отправляет заявку в
Telegram через `POST /api/lead`.

## Публикация на GitHub Pages

Репозиторий: <https://github.com/makhailya/massage_site> (публичный, GitHub Free).

1. Отправить изменения в ветку `main` (после проверки и подтверждения).
2. В GitHub открыть **Settings → Pages**.
3. В **Build and deployment → Source** выбрать **Deploy from a branch**.
4. Выбрать ветку **`main`** и папку **`/ (root)`**, нажать **Save**.
5. Через 1–2 минуты сайт будет доступен по адресу:
   <https://makhailya.github.io/massage_site/>

Сборка не нужна: GitHub Pages публикует файлы как есть. `.nojekyll` уже
добавлен, чтобы файлы и каталоги с `_` в начале имени не исключались.

### Важно про существующий деплой

`.github/workflows/deploy.yml` — отдельный workflow для FastAPI на
self-hosted runner. Он запускается при пуше в `main` и деплоит серверную
версию. GitHub Pages от него не зависит. Если серверный деплой больше не
нужен, workflow можно отключить отдельно в **Actions**.

## Проверки

```bash
npx html-validate index.html
```

Перед публикацией проверено:

- HTML — без ошибок (html-validate и W3C Nu Validator);
- нет горизонтального скролла на 360, 390, 768, 1024 и 1440 px;
- нет ошибок в консоли браузера;
- все локальные пути относительные и открываются из поддиректории
  (`/massage_site/`), как на GitHub Pages;
- контент виден без JavaScript, при `prefers-reduced-motion` и при
  недоступном CDN;
- axe-core (WCAG 2.1/2.2 AA) — без нарушений.

## Технологии и внешние ресурсы

- Шрифты: Onest и Unbounded через Google Fonts (лицензия SIL OFL).
- Анимации: GSAP 3.12.5 и ScrollTrigger с cdnjs (стандартная лицензия GSAP).
  При недоступном CDN контент остаётся видимым.
- favicon и портрет — локальные файлы в `assets/images/`.

## Секреты

`.env` не коммитится (см. `.gitignore`). В нём хранятся
`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` и `CLOUDFLARED_TUNNEL_TOKEN`.
Не добавляйте реальные значения в `.env.example`, README и код.
