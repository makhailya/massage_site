# Massage Site

Веб-сайт массажиста Ильи Маханёка: лендинг, каталог услуг, онлайн-запись клиентов, личный кабинет и админ-панель.

Проект сделан на Django и запускается в Docker-связке `Django + Gunicorn + Nginx + PostgreSQL`.

## Возможности

- Главная страница с описанием услуг и контактами
- Каталог услуг с ценами, длительностью и описанием
- Регистрация и вход пользователей
- Онлайн-запись на сеанс
- Личный кабинет клиента с историей записей
- Админ-панель Django для управления услугами и заявками
- Docker Compose окружение для локального запуска и деплоя
- Тесты на pytest с отчетом покрытия

## Стек

| Часть | Технологии |
| --- | --- |
| Backend | Python 3.13, Django 6 |
| Database | PostgreSQL 15 |
| Web server | Gunicorn, Nginx |
| Frontend | HTML, CSS, Django Templates |
| Infra | Docker, Docker Compose |
| Tests | pytest, pytest-django, pytest-cov |

## Быстрый старт

### 1. Клонировать проект

```bash
git clone https://github.com/makhailya/massage_site.git
cd massage_site
```

### 2. Создать `.env`

Создай файл `.env` в корне проекта:

```env
POSTGRES_DB=massage_db
POSTGRES_USER=massage_user
POSTGRES_PASSWORD=massage_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=change-me-for-local-development
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### 3. Запустить контейнеры

```bash
docker compose up --build -d
```

### 4. Применить миграции

```bash
docker compose exec web python manage.py migrate
```

### 5. Создать администратора

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Открыть сайт

- Сайт: [http://localhost:8000](http://localhost:8000)
- Админ-панель: [http://localhost:8000/admin](http://localhost:8000/admin)

## Команды разработки

Запуск проекта:

```bash
docker compose up -d
```

Остановка проекта:

```bash
docker compose down
```

Просмотр логов:

```bash
docker compose logs -f
```

Просмотр логов конкретного сервиса:

```bash
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f db
```

Повторная сборка после изменений зависимостей или Dockerfile:

```bash
docker compose up --build -d
```

Сборка статики:

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## Тесты

Локальный запуск:

```bash
poetry run pytest
```

Локальный запуск с покрытием:

```bash
poetry run pytest --cov=. --cov-report=term-missing
```

Запуск тестов внутри Docker:

```bash
docker compose exec web pytest --cov=. --cov-report=term-missing
```

Текущий результат:

```text
15 passed
TOTAL coverage: 88%
```

## Архитектура Docker

Проект поднимает три сервиса:

| Сервис | Назначение |
| --- | --- |
| `db` | PostgreSQL 15 |
| `web` | Django-приложение под Gunicorn на порту `8000` внутри Docker-сети |
| `nginx` | Внешний вход, проксирует запросы в `web` и отдает статику |

Снаружи сайт доступен через Nginx:

```text
localhost:8000 -> nginx:80 -> web:8000
```

## Production

Для production рекомендуется задать более строгий `.env`:

```env
POSTGRES_DB=massage_db
POSTGRES_USER=massage_user
POSTGRES_PASSWORD=strong-production-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=makhailya.ru,localhost,127.0.0.1,SERVER_IP
CSRF_TRUSTED_ORIGINS=https://makhailya.ru,http://makhailya.ru,http://SERVER_IP
```

Типовой деплой:

```bash
git pull
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

Если сайт должен открываться на стандартном HTTP-порту сервера, поменяй публикацию Nginx в `docker-compose.yml`:

```yaml
ports:
  - "80:80"
```

После изменения портов пересоздай контейнер:

```bash
docker compose up -d
```

## Cloudflare Tunnel

Cloudflare Tunnel можно добавить отдельно, если нужно открыть сайт в интернет без прямого проброса портов.

Пример сервиса для `docker-compose.yml`:

```yaml
cloudflared:
  image: cloudflare/cloudflared:latest
  restart: unless-stopped
  command: tunnel --no-autoupdate run --token YOUR_CLOUDFLARE_TUNNEL_TOKEN
  depends_on:
    - nginx
  networks:
    - app-network
```

В настройках Cloudflare Tunnel укажи публичное имя:

```text
makhailya.ru -> HTTP -> nginx:80
```

## Структура проекта

```text
massage_site/
├── booking/              # Записи клиентов
├── config/               # Настройки Django
├── nginx/                # Конфигурация Nginx
├── services/             # Услуги массажа
├── static/               # Исходные статические файлы
├── templates/            # HTML-шаблоны
├── users/                # Регистрация пользователей
├── docker-compose.yml    # Docker Compose окружение
├── Dockerfile            # Образ Django/Gunicorn
├── manage.py
├── pyproject.toml        # Зависимости Poetry
└── README.md
```

## Полезные URL

- `/` — главная страница
- `/services/` — список услуг
- `/booking/` — онлайн-запись
- `/account/` — личный кабинет
- `/accounts/login/` — вход
- `/accounts/register/` — регистрация
- `/admin/` — Django admin

## Статус

Проект находится в стадии MVP: основная бизнес-логика работает, тесты проходят, Docker-окружение настроено для локального запуска и дальнейшего деплоя.

