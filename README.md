# 💆 Сайт массажиста — Илья Маханек

Веб-сайт для продвижения услуг массажа с онлайн-записью клиентов.

## 🚀 Возможности

- Каталог услуг с ценами
- Онлайн-запись на сеанс
- Личный кабинет клиента
- Панель администратора

## 🛠 Стек технологий

- **Backend:** Django 6, PostgreSQL
- **Frontend:** HTML, CSS
- **Инфраструктура:** Docker, Docker Compose
- **Тесты:** pytest, покрытие 88%

## ⚡️ Быстрый старт

### 1. Клонируй репозиторий
```bash
git clone https://github.com/ТВОЙ_НИКНЕЙМ/massage_site.git
cd massage_site
```

### 2. Создай .env файл
```bash
POSTGRES_DB=massage_db
POSTGRES_USER=massage_user
POSTGRES_PASSWORD=massage_pass
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=твой-секретный-ключ
DEBUG=True
```

### 3. Запусти проект
```bash
docker-compose up --build
```

### 4. Примени миграции
```bash
docker-compose exec web python manage.py migrate
```

### 5. Создай администратора
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Открой браузер
http://localhost:8000        — сайт
http://localhost:8000/admin  — админ-панель

## 🧪 Запуск тестов
```bash
docker-compose exec web pytest --cov=. --cov-report=term-missing
```

## 📁 Структура проекта
massage_site/
├── config/          — настройки Django
├── services/        — приложение услуг
├── booking/         — приложение записей
├── users/           — приложение пользователей
├── templates/       — HTML шаблоны
├── docker-compose.yml
├── Dockerfile
└── README.md
