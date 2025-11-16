# README.md

# PR Reviewer Assignment Service

Сервис для управления командами, пользователями и назначением ревьюверов на Pull Request.

## Возможности

* Управление пользователями и командами
* Создание PR с автоматическим назначением до 2 ревьюверов из команды автора
* Переназначение ревьювера
* Получение списка PR, где пользователь является ревьювером
* Merge PR с идемпотентной логикой
* Полностью соответствует OpenAPI 3.0.3 спецификации

## Технологии

* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy / SQLModel
* Pydantic
* Alembic миграции
* Docker + Docker Compose

## Запуск

1. Склонировать репозиторий

```bash
git clone <repo-url>
cd <repo-folder>
```

2. Поднять сервис через Docker Compose

```bash
docker-compose up --build
```

3. Сервис будет доступен на `http://localhost:8080`

## Документация API

* Swagger UI: `http://localhost:8080/docs`
* ReDoc: `http://localhost:8080/redoc`

## Миграции

При старте Docker Compose миграции применяются автоматически.

## Структура проекта

* `app/main.py` — точка входа FastAPI
* `app/models.py` — SQLAlchemy/SQLModel модели
* `app/scheme.py` — Pydantic схемы
* `app/routers/` — endpoints
* `app/crud/` — бизнес-логика работы с базой
* `alembic/` — миграции базы данных
