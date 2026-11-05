# MAKHAILYA

Статический сайт на HTML, CSS и JavaScript. GitHub Pages публикует три страницы
без этапа сборки.

| Адрес на GitHub Pages | Страница |
| --- | --- |
| `/massage_site/` | Главная с выбором направления — массаж или ремонт техники |
| `/massage_site/massage/` | Услуги массажа, цены, информация о специалисте и контакты |
| `/massage_site/repair/` | Ремонт и настройка компьютеров и смартфонов, обслуживание ПО и домашних сетей |

Старые ссылки на главную с якорями `#services`, `#about`, `#help`, `#contact`
и `#top` открывают соответствующие разделы страницы массажа с исходными
параметрами запроса. При отключённом JavaScript на главной доступны обычные
ссылки на оба направления и на разделы массажа.

## Структура

| Путь | Назначение |
| --- | --- |
| `index.html`, `massage/index.html`, `repair/index.html` | Три публичные страницы |
| `css/home.css`, `css/style.css`, `css/repair.css` | Стили главной, массажа и ремонта соответственно |
| `js/home.js` | Перенаправление старых якорных ссылок |
| `js/script.js` | Анимации страницы массажа через GSAP и ScrollTrigger |
| `assets/fonts/` | Локальные шрифты Onest и Unbounded и их лицензии SIL OFL |
| `assets/images/` | Favicon, иллюстрации, портрет и изображения для предпросмотра ссылок |
| `sitemap.xml` | Карта трёх публичных страниц |
| `.github/workflows/pages.yml` | Публикация статического сайта |
| `app.py`, `static/` | FastAPI backend для локального запуска формы заявки |
| `Dockerfile`, `docker-compose.yml` | Опциональная конфигурация Docker для FastAPI и Cloudflare Tunnel; не используется GitHub Pages |

## Локальный запуск

Для просмотра статического сайта запустите из корня репозитория:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Откройте <http://localhost:8000/>. Шрифты и изображения загружаются локально.
На странице массажа GSAP и ScrollTrigger загружаются с cdnjs. При недоступном
CDN контент остаётся видимым. Портрет использует адаптивные WebP с резервным JPEG.

Для локального запуска FastAPI (этот backend не входит в публикацию GitHub Pages)
установите зависимости в активное виртуальное окружение и настройте `.env` по
`.env.example`:

```bash
uv pip install -r requirements-dev.txt
uvicorn app:app --reload
```

Откройте <http://localhost:8000/>. Форма отправляет заявку в Telegram через
`POST /api/lead`. Оба примера используют порт 8000, поэтому запускайте их по
очереди.

## Публикация на GitHub Pages

В настройках репозитория откройте **Settings → Pages → Build and deployment →
Source** и выберите **GitHub Actions**. Workflow **Publish landing to GitHub
Pages** запускается при отправке изменений в `main` по путям из `pages.yml`.
Ручной запуск доступен в **Actions → Publish landing to GitHub Pages →
Run workflow → main**.

Workflow копирует `index.html`, `sitemap.xml` и каталоги `massage/`, `repair/`,
`css/`, `js/`, `assets/` в отдельный пакет и передаёт его GitHub Pages.
При добавлении нового публичного файла или каталога верхнего уровня обновите
список копирования и пути запуска в `pages.yml`. Backend-код, `static/`, файлы
Docker и `.env` не входят в пакет и не развёртываются на этом сайте.

После публикации проверьте [главную страницу](https://makhailya.github.io/massage_site/)
и [карту сайта](https://makhailya.github.io/massage_site/sitemap.xml).

## Настройки локального FastAPI

Локальный `.env` исключён из Git. FastAPI использует в нём
`TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`; конфигурация Cloudflare Tunnel
использует `CLOUDFLARED_TUNNEL_TOKEN`. В `.env.example` храните только примеры
значений.
