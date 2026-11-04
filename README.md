# Илья Маханек — массаж · Верхняя Пышма

Одностраничный лендинг массажиста. Основная версия — **статический сайт**
(HTML5, CSS3, Vanilla JS) без сборки, backend и базы данных. Публикуется на
GitHub Pages.

В репозитории также сохранена прежняя версия на FastAPI (`app.py` + `static/`)
с формой заявки в Telegram. Новый процесс публикации Pages не включает её
в публичный пакет.

## Структура

```
index.html              главная страница для GitHub Pages
sitemap.xml             карта сайта для поисковых систем
css/style.css           стили
js/script.js            анимации появления (GSAP + ScrollTrigger)
assets/fonts/           локальные шрифты и лицензии
assets/images/hero*     портрет в WebP и резервный JPEG
assets/images/favicon.svg
.github/workflows/pages.yml   публикация актуального лендинга
.github/workflows/deploy.yml  отдельный серверный деплой FastAPI
.nojekyll               отключает Jekyll при публикации из ветки
static/                 прежняя версия, которую раздаёт FastAPI
app.py                  FastAPI: POST /api/lead → Telegram
```

## Локальный запуск

Статическая версия (рекомендуется):

```bash
python3 -m http.server 8000
```

Открыть <http://localhost:8000/>. Шрифты загружаются локально. Интернет нужен
для GSAP; без него содержимое страницы остаётся доступным.

FastAPI-версия (опционально, нужны Python и `.env`):

```bash
uv pip install -r requirements-dev.txt
uvicorn app:app --reload
```

Открыть <http://localhost:8000>. Форма на этой версии отправляет заявку в
Telegram через `POST /api/lead`.

## Публикация на GitHub Pages

Репозиторий: <https://github.com/makhailya/massage_site> (публичный, GitHub Free).

При первом переходе на новый процесс публикации:

1. В GitHub открыть **Settings → Pages → Build and deployment → Source**
   и выбрать **GitHub Actions**.
2. Отправить согласованные изменения в ветку `main`. Изменения в `index.html`,
   `sitemap.xml`, `css/`, `js/`, `assets/` или самом `pages.yml` запустят публикацию.
   Если workflow уже в `main`, его также можно запустить вручную:
   **Actions → Publish landing to GitHub Pages → Run workflow → main**.
3. Дождаться успешного запуска и проверить главную страницу по адресу
   <https://makhailya.github.io/massage_site/>. Старый адрес
   `/massage_site/static/index.html` после публикации должен отвечать `404`.

Сборка не нужна. `.github/workflows/pages.yml` копирует `index.html`,
`sitemap.xml`, `css/`, `js/` и `assets/` в отдельный пакет. При добавлении
нового публичного файла в корне лендинга его нужно явно добавить в пакет
и в список путей, которые запускают публикацию.

После публикации карта сайта будет доступна по адресу
<https://makhailya.github.io/massage_site/sitemap.xml>.

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

- Шрифты: локальные вариативные WOFF2 — Onest 400–500 и Unbounded 500–700.
  Кириллица, латиница, цифры и пунктуация включены в два файла общим размером
  около 79 КиБ. Запросы к Google Fonts не нужны. Источники и лицензии SIL OFL
  находятся в `assets/fonts/`.
- Анимации: GSAP 3.12.5 и ScrollTrigger с cdnjs (стандартная лицензия GSAP).
  При недоступном CDN контент остаётся видимым.
- Favicon и портрет лежат в `assets/images/`. Браузер выбирает портрет WebP
  шириной 360, 576 или 675 px. JPEG служит резервом для браузеров без WebP.

## Секреты

`.env` не коммитится (см. `.gitignore`). В нём хранятся
`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` и `CLOUDFLARED_TUNNEL_TOKEN`.
Не добавляйте реальные значения в `.env.example`, README и код.
