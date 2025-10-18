# WorkCommunities Backend

Бэкенд сервиса сообществ и компаний для публикаций, историй и событий. Основан на FastAPI, асинхронном SQLAlchemy и разделённой на слои архитектуре (domain → usecases → infrastructure → presentation).

Развёртывание: сервис поднят на Reg.ru двумя способами — через Docker Compose и через pm2 с tuna для доступа по HTTPS. Публичный доступ: http://91.197.99.176:8000 (Swagger: http://91.197.99.176:8000/docs).

Содержание
- [Стек](#стек)
- [Архитектура](#архитектура)
- [API и аутентификация](#api-и-аутентификация)
- [Запуск через Docker](#запуск-через-docker)
- [Локальный запуск без Docker](#локальный-запуск-без-docker)
- [Переменные окружения](#переменные-окружения)
- [Данные и миграции](#данные-и-миграции)
- [Демо-скрипты](#демо-скрипты)
- [Полезные эндпоинты](#полезные-эндпоинты)
- [Структура проекта](#структура-проекта)

## Стек
- FastAPI — веб‑фреймворк и OpenAPI-документация.
- SQLAlchemy (async) + asyncpg — доступ к PostgreSQL.
- База данных: PostgreSQL 15 (сервис `db` в `docker-compose.yml`).
- PyJWT — выпуск и верификация JWT‑токенов.
- Passlib (bcrypt) — хеширование паролей для администраторов.
- Pydantic Settings — конфигурация через переменные окружения и .env.
- Uvicorn — ASGI‑сервер.

## Архитектура
Проект разделён на слои с чёткими границами и зависимостями только «вниз»:
- Domain (`app/domain`) — сущности и протоколы репозиториев, независимые от инфраструктуры.
- Use cases (`app/usecases`) — прикладная бизнес‑логика (авторизация, контент, компании и т. д.).
- Infrastructure (`app/infrastructure`) — реализация репозиториев (SQLAlchemy), сервисы хранения медиа.
- Presentation (`app/presentation`) — HTTP‑слой: эндпоинты FastAPI и Pydantic‑схемы.
- Adapters (`app/adapters`) — адаптеры к инфраструктуре (например, создание `engine`, `session`).

Точки входа:
- Приложение FastAPI: `backend/app/main.py` — инициализация API, создание таблиц и «лёгкие» миграции при старте.
- Маршрутизация API: `backend/app/presentation/api/router.py` — подключение всех подсекций (`auth`, `media`, `content`, `events`, `companies`, `communities`, `profiles`, `reference`, `users`).

## API и аутентификация
- База: FastAPI, корневой роутер — `backend/app/presentation/api/router.py`.
- Swagger UI: `GET /docs`, ReDoc: `GET /redoc`.
- Health: `GET /health` → `{ "status": "ok" }`.
- Аутентификация: Bearer JWT в заголовке `Authorization: Bearer <token>`.
  - OTP‑логин для студентов и компаний: `/auth/otp/request`, `/auth/otp/verify`, а также `/auth/company/otp/*`.
  - В dev‑режиме код OTP фиксированный: `11111` (см. `app/usecases/auth.py`).
  - Токен содержит `sub` (user id), `role` (`student` | `company` | `admin`), при необходимости `company_id`.
  - Гварды ролей: `role_required(...)` и `get_current_company` (см. `app/core/deps.py`).
- Медиа: `POST /media/upload` (multipart) сохраняет файл на локальном сторадже (`/data/media`) и возвращает `{id, url, ...}`;
  `GET /media/{id}` — отдаёт файл.

Ключевые зоны API (кратко)
- Компании (`/companies`): список, детали, «мои», обновление «моей» компании, подписки на компании.
- Сообщества (`/communities`): список, создание/обновление (роль `company`), подписки, посты сообщества.
- Контент (`/content`): посты и истории; единый фид контента `GET /content/posts` (посты и события, сортировка по `created_at`).
- События (`/events`): создание (роль `company`), листинги «предстоящих», «моих», участие.
- Профиль (`/profiles`): «мой» профиль, обновление, скиллы/статусы.
- Справочники (`/reference`): сферы, навыки, статусы.

## Запуск через Docker
Требования: Docker, Docker Compose. Корневой `docker-compose.yml` билдит API из директории `backend/` и поднимает PostgreSQL.

- Старт/обновление (detached)
```
docker compose up -d --build
```
- Проверка статуса/логов
```
docker compose ps
docker compose logs -f api
```
- Перезапуск API
```
docker compose restart api
```
- Остановка (аккуратно в dev)
```
docker compose down
```

После старта: API доступен на `http://localhost:8000` (Swagger: `/docs`). База — сервис `db` (PostgreSQL 15) с дефолтными параметрами из compose.

Примечание по медиа: по умолчанию файлы сохраняются внутри контейнера (`/data/media`). Для постоянного хранения добавьте volume‑маппинг в `api` и соответствующий `volume`.

## Локальный запуск без Docker
Требования: Python 3.11+, PostgreSQL 15+.

1) Установить зависимости
```
cd backend
pip install -r requirements.txt
```
2) Настроить окружение (см. «Переменные окружения»). Для local‑базы пример:
```
export DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/communities
```
3) Запустить сервер
```
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Переменные окружения
Конфигурация читается из окружения и `.env` (см. `backend/app/core/config.py`). Важные параметры:
- `DATABASE_URL` — строка подключения SQLAlchemy (по умолчанию в Docker: `postgresql+asyncpg://postgres:postgres@db:5432/communities`).
- `JWT_SECRET` — секрет для подписи JWT.
- `JWT_ALG` — алгоритм подписи (по умолчанию `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES` — время жизни access‑токена (минуты).
- `OTP_TTL_SECONDS` — TTL кода OTP.
- `ADMIN_SIGNUP_TOKEN` — секрет для регистрации админа.

## Данные и миграции
- Инициализация схемы: при старте сервиса создаются таблицы (`Base.metadata.create_all`).
- Лёгкие миграции: `backend/app/migrations/auto.py` — добавляет/досоздаёт необходимые колонки для обратной совместимости.
- Медиа‑хранилище: локальные файлы через `LocalFileStorage` в `/data/media` (volume Docker Compose).

Запуск миграций вручную (опционально, внутри контейнера):
```
docker compose exec api python -m app.migrations.auto
```

## Основные скрипты
- Сброс и наполнение демо‑данными: `backend/app/scripts/reset_and_seed_demo.py`
  - Действия: очистка основной части данных (с сохранением справочников), загрузка моковых картинок, создание пользователей/профилей, компаний/сообществ, поста и событий.
  - Требует запущенного API (для `POST /media/upload`).
  - Рекомендованный запуск внутри контейнера API:
```
docker compose exec api python -m app.scripts.reset_and_seed_demo --base-url http://localhost:8000 --media-dir app/scripts/media_mockups
```

- Скрипт E2E для компании: `backend/app/scripts/e2e_company_flow.py`
  - Поток: OTP‑аутентификация компании → создание сообщества → загрузка медиа → пост → сториз → событие → проверки.
  - Запуск внутри контейнера:
```
docker compose exec api python -m app.scripts.e2e_company_flow --base-url http://localhost:8000 --verbose
```

Дополнительно: при необходимости можно исполнять скрипты и с хоста, перейдя в `backend/` и настроив `DATABASE_URL`/`BASE_URL`.

## Полезные эндпоинты
- Swagger: `GET /docs`, ReDoc: `GET /redoc`.
- Health: `GET /health`.
- Загрузка медиа: `POST /media/upload` (multipart form‑data).
- Компании: `GET /companies`, «моя компания»: `GET /companies/me` (роль `company`).
- Сообщества: `GET /communities`, посты сообщества: `GET /communities/{id}/posts`.
- Кейсы сообществ:
  - Создать кейс (роль `company`): `POST /communities/{id}/cases` с телом `{ title, date, solutions_count, description? }`.
  - Удалить кейс (роль `company`): `DELETE /communities/{id}/cases/{case_id}`.
  - Детали сообщества возвращают список кейсов: `GET /communities/{id}` → `cases[]`.
- Единый фид контента: `GET /content/posts` (посты и события).

## Структура проекта
- `backend/app/main.py` — приложение FastAPI, стартовые миграции.
- `backend/app/presentation/api` — эндпоинты (роуты), точка подключения — `router.py`.
- `backend/app/presentation/schemas` — Pydantic‑схемы запросов/ответов.
- `backend/app/usecases` — бизнес‑логика (авторизация, контент, компании и т. п.).
- `backend/app/infrastructure/repos` — репозитории (SQLAlchemy, модели в `sql_models.py`).
- `backend/app/infrastructure/services` — сервисы (локальное хранилище медиа и др.).
- `backend/app/adapters` — БД‑адаптеры (`engine`, `session`).
- `backend/app/core` — конфигурация, зависимости авторизации и безопасность (JWT, роли).
- `backend/app/scripts` — вспомогательные и демо‑скрипты.

Если нужна помощь с развертыванием на окружении CI/CD, тестовыми данными или дополнительной документацией (ER‑диаграмма, коллекция для Postman) — дайте знать.
