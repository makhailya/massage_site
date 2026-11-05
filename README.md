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
| `app.py`, `static/` | Серверная версия на FastAPI с формой заявки в Telegram |
| `Dockerfile`, `docker-compose.yml` | Контейнеры серверной версии и Cloudflare Tunnel |
| `.github/workflows/deploy.yml` | Отдельный серверный деплой |

## Локальный запуск

Для просмотра статического сайта запустите из корня репозитория:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Откройте <http://localhost:8000/>. Шрифты и изображения загружаются локально.
На странице массажа GSAP и ScrollTrigger загружаются с cdnjs. При недоступном
CDN контент остаётся видимым. Портрет использует адаптивные WebP с резервным JPEG.

Для отдельного запуска FastAPI установите зависимости в активное виртуальное
окружение и настройте `.env` по `.env.example`:

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
список копирования и пути запуска в `pages.yml`. Серверный код, `static/`,
файлы Docker и `.env` находятся за пределами этого пакета.

После публикации проверьте [главную страницу](https://makhailya.github.io/massage_site/)
и [карту сайта](https://makhailya.github.io/massage_site/sitemap.xml).

## Серверный деплой и секреты

`.github/workflows/deploy.yml` запускается на self-hosted runner при изменении
серверных файлов в `main`. На сервере Docker Compose собирает и запускает
FastAPI и поддерживает отдельный контейнер Cloudflare Tunnel. Публикация на
GitHub Pages выполняется независимо.

Для SSH-деплоя добавьте в **Settings → Secrets and variables → Actions** секреты
`SSH_PRIVATE_KEY`, `SERVER_HOST`, `SERVER_USER` и `SSH_KNOWN_HOSTS`. Чтобы получить
публичный host key, откройте сервер через доверенную консоль провайдера или другой
проверенный административный канал и выполните:

```bash
sudo sshd -T | awk '$1 == "hostkey" {print $2}'
sudo cat /etc/ssh/ssh_host_ed25519_key.pub
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

Первая команда показывает пути host key, которые настроены в `sshd`. В примере
используется Ed25519; подставьте путь из этого списка в следующие две команды.
Скопируйте только публичную строку и независимо сравните её отпечаток
`SHA256:...` с отпечатком, полученным по отдельному доверенному каналу (например,
из консоли провайдера или от администратора сервера). Не копируйте приватный
файл `ssh_host_*_key`. Для обычного порта 22 значение `SSH_KNOWN_HOSTS` должно
содержать строку `SERVER_HOST ТИП_КЛЮЧА ПУБЛИЧНАЯ_ЧАСТЬ`.
Для другого порта укажите поле узла как `[SERVER_HOST]:ПОРТ` и создайте секрет
`SSH_PORT` с тем же номером. При отсутствии `SSH_PORT` используется порт 22.
Workflow проверяет формат known_hosts и наличие записи именно для заданного
узла и порта до SSH-подключения; host key проверяется с
`StrictHostKeyChecking=yes`.

Локальный `.env` исключён из Git. В нём хранятся `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID` и `CLOUDFLARED_TUNNEL_TOKEN`. Для `.env.example` используйте
только примеры значений.
