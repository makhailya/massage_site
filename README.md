# MAKHAILYA

Публичный сайт полностью статический: HTML, CSS, JavaScript и ресурсы. GitHub
Pages публикует три страницы без этапа сборки.

| Адрес на GitHub Pages | Страница |
| --- | --- |
| `/massage_site/` | Главная с выбором направления — массаж или ремонт техники |
| `/massage_site/massage/` | Услуги массажа, цены, информация о специалисте и контакты |
| `/massage_site/repair/` | Ремонт и настройка компьютеров и смартфонов, обслуживание ПО и домашних сетей |

Старые ссылки на главную с якорями `#services`, `#about`, `#help`, `#contact`
и `#top` открывают соответствующие разделы страницы массажа с исходными
параметрами запроса. При отключённом JavaScript на главной доступны обычные
ссылки на оба направления и разделы массажа.

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
| `.github/workflows/pages.yml` | Публикация статического сайта на GitHub Pages |
| `app.py`, `static/` | Необязательное FastAPI-приложение: отдельно отдаёт `static/index.html` и ресурсы из `static/` |
| `requirements.txt`, `requirements-dev.txt`, `tests/test_app.py` | Зависимости приложения, разработки и существующие тесты |
| `Dockerfile`, `docker-compose.yml` | Необязательная конфигурация Docker для FastAPI и Cloudflare Tunnel; GitHub Pages её не использует |
| `.env.example` | Образец переменных окружения без секретных значений |

## Локальный просмотр публичного сайта

Из корня репозитория запустите простой HTTP-сервер:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Откройте <http://localhost:8000/>. Шрифты и изображения загружаются локально.
GSAP и ScrollTrigger на странице массажа загружаются с cdnjs; при недоступном
CDN контент остаётся видимым. Портрет использует адаптивные WebP с резервным
JPEG.

## Необязательный локальный FastAPI

FastAPI — отдельный компонент для локального запуска формы заявки. Его маршрут
`/` отдаёт `static/index.html`, а не корневой `index.html`, который GitHub Pages
публикует как главную. FastAPI, каталог `static/` и Docker-файлы не входят в
пакет публичного сайта.

Создайте виртуальное окружение и установите зависимости из корня репозитория:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
cp -n .env.example .env
```

Заполните в `.env` значения `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`. Затем
загрузите переменные в текущую оболочку и запустите приложение:

```bash
set -a
. ./.env
set +a
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Команда `. ./.env` читает файл в текущую оболочку, а `set -a` экспортирует
заданные в нём переменные для FastAPI; менять исходный код не нужно. Локальный
файл `.env` исключён из Git. Не помещайте в репозиторий реальные токены.
Если файл загружается через shell, значения со специальными символами
(например, пробелами, `$` или `#`) заключайте в одинарные кавычки или
экранируйте по правилам shell.
Переменная `CLOUDFLARED_TUNNEL_TOKEN` из `.env.example` нужна только для
необязательной конфигурации Cloudflare Tunnel в Docker. После запуска откройте
<http://localhost:8000/>. Форма отправляет заявку в Telegram через
`POST /api/lead`. Для просмотра публичного сайта и FastAPI используется один
порт 8000 — запускайте их по очереди.

## Тесты

После установки зависимостей и активации виртуального окружения запустите
существующие тесты из корня репозитория:

```bash
python -m pytest
```

## Публикация на GitHub Pages

В настройках репозитория откройте **Settings → Pages → Build and deployment →
Source** и выберите **GitHub Actions**. Workflow **Publish landing to GitHub
Pages** запускается при отправке изменений в `main` по путям, указанным в
`pages.yml`. Ручной запуск доступен в **Actions → Publish landing to GitHub
Pages → Run workflow → main**.

Workflow копирует корневые файлы `index.html` и `sitemap.xml`, а также каталоги
`massage/`, `repair/`, `css/`, `js/` и `assets/` целиком в отдельный пакет
GitHub Pages. Если добавите публичный файл или каталог верхнего уровня,
обновите список копирования и пути запуска в `pages.yml`. Backend-код,
`static/`, Docker-файлы и `.env` в пакет не входят.

После публикации проверьте [главную страницу](https://makhailya.github.io/massage_site/)
и [карту сайта](https://makhailya.github.io/massage_site/sitemap.xml).
