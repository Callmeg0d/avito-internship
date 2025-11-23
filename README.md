# PR Reviewer Assignment Service

Сервис для автоматического назначения ревьюверов на Pull Request'ы.

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic (миграции)

## Запуск

### Через Docker Compose

```bash
docker-compose up
```

Сервис будет доступен на `http://localhost:8080`

Документация (Swagger) на `http://localhost:8080/docs`


## Тестовые данные

Для быстрого тестирования можно создать тестовые данные:

```bash
python test_data.py
```

Это создаст:
- Команду "backend" с 3 пользователями (Alice, Bob, Charlie)
- 2 PR с автоматически назначенными ревьюверами

## API

Документация доступна по адресу `http://localhost:8080/docs` после запуска сервиса.

Основные эндпоинты:
- `POST /team/add` - создать команду
- `GET /team/get` - получить команду
- `POST /users/setIsActive` - установить активность пользователя
- `POST /pullRequest/create` - создать PR и назначить ревьюверов
- `POST /pullRequest/merge` - пометить PR как MERGED
- `POST /pullRequest/reassign` - переназначить ревьювера
- `GET /users/getReview` - получить PR'ы пользователя
- `GET /stats/assignments` - статистика назначений по пользователям

## Линтер и проверка типов

Проект использует **mypy** для статической проверки типов.

### Конфигурация

Конфигурация mypy находится в файле `mypy.ini`:
- Включены предупреждения о неиспользованных конфигурациях
- Игнорируются отсутствующие импорты для внешних библиотек (SQLAlchemy, FastAPI и т.д.)
- Исключены директории миграций Alembic

### Запуск проверки типов

```bash
mypy app/
```

Или для проверки всего проекта:
```bash
mypy .
```

## Структура проекта

```
app/
  models/          # SQLAlchemy модели БД
  repositories/    # Слой доступа к данным
  services/        # Бизнес-логика
  schemas/         # Pydantic схемы для API
  routers/         # FastAPI роутеры
  exceptions.py    # Исключения
  config.py        # Конфигурация
  database.py      # Настройка БД
alembic/           # Миграции БД
app/main.py        # Точка входа FastAPI
.env               # Переменные окружения (создать на основе .env.example)
mypy.ini           # Конфигурация mypy
```

