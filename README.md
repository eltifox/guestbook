# Guestbook

Гостевая книга: FastAPI + PostgreSQL. Образ собирается в GitHub Actions и публикуется в ghcr.io.

## Запуск

1. Скопировать шаблон секретов и задать пароль:
   cp .env.example .env
2. Запустить сервис и базу:
   docker compose up --build -d
3. Проверить: http://localhost:8000/health
   Документация API: http://localhost:8000/docs

## Версии и релизы

- Push в main: образ ghcr.io/eltifox/guestbook:latest
- Тег vX.Y.Z (semver): образ ghcr.io/eltifox/guestbook:X.Y.Z
- История изменений: CHANGELOG.md

Выпуск релиза:

    git tag v1.2.0
    git push origin v1.2.0

## Запуск конкретной версии

    APP_VERSION=1.1.0 docker compose pull app
    APP_VERSION=1.1.0 docker compose up -d --no-build

Аварийные ситуации и откат: RUNBOOK.md
